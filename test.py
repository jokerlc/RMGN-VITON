import time
from options.test_options import TestOptions
from data.data_loader_test import CreateDataLoader
from models.networks import ResUnetGenerator, load_checkpoint
from models.afwm import AFWM
from models.rmgn_generator import RMGNGenerator
import torch.nn as nn
import os
import numpy as np
import torch
import cv2
import torch.nn.functional as F

opt = TestOptions().parse()

start_epoch, epoch_iter = 1, 0

data_loader = CreateDataLoader(opt)
dataset = data_loader.load_data()
dataset_size = len(data_loader)
print(dataset_size)

warp_model = AFWM(opt, 3)
warp_model.eval()
warp_model.cuda()
load_checkpoint(warp_model, opt.warp_checkpoint, opt.load_hr_author)

gen_model = RMGNGenerator(multilevel=opt.multilevel, predmask=opt.predmask)
gen_model.eval()
gen_model.cuda()
load_checkpoint(gen_model, opt.gen_checkpoint, opt.load_hr_author)

total_steps = (start_epoch-1) * dataset_size + epoch_iter
step = 0
step_per_batch = dataset_size / opt.batchSize

for epoch in range(1,2):
    
    for i, data in enumerate(dataset, start=epoch_iter):
        iter_start_time = time.time()
        total_steps += opt.batchSize
        epoch_iter += opt.batchSize

        real_image = data['image']
        clothes = data['clothes']
        ##edge is extracted from the clothes image with the built-in function in python
        edge = data['edge']
        edge = torch.FloatTensor((edge.detach().numpy() > 0.5).astype(np.int))
        clothes = clothes * edge
        flow_out = warp_model(real_image.cuda(), clothes.cuda())
        warped_cloth, last_flow, = flow_out
        warped_edge = F.grid_sample(edge.cuda(), last_flow.permute(0, 2, 3, 1),
                          mode='bilinear', padding_mode='zeros')
        
        gen_inputs_clothes = torch.cat([warped_cloth, warped_edge], 1)
        gen_inputs_persons = real_image.cuda()
        
        gen_outputs, out_L1, out_L2, M_list = gen_model(gen_inputs_persons, gen_inputs_clothes)
        
        if opt.predmask:

            p_rendered, m_composite = torch.split(gen_outputs, [3, 1], 1)
            
            p_rendered = torch.tanh(p_rendered)
            m_composite = torch.sigmoid(m_composite)
            m_composite = m_composite * warped_edge
            p_tryon = warped_cloth * m_composite + p_rendered * (1 - m_composite)
            
        else:

            p_rendered = gen_outputs
            p_rendered = torch.tanh(p_rendered)
            p_tryon = p_rendered
        
        
        path = 'test_results/' + opt.name
        os.makedirs(path, exist_ok=True)
        sub_path = path + '/RMGN'
        os.makedirs(sub_path,exist_ok=True)
        
        if step % 1 == 0:
            a = real_image.float().cuda()
            b= clothes.cuda()
            c = p_tryon
            d = p_rendered
            e = warped_cloth
            f = torch.cat([m_composite,m_composite,m_composite], 1) 
            g = torch.cat([warped_edge,warped_edge,warped_edge], 1)
            k = torch.cat([M_list[-1].cuda(), M_list[-1].cuda(), M_list[-1].cuda()], 1)
            combine = torch.cat([c[0]], 2).squeeze()
            
            cv_img=(combine.permute(1,2,0).detach().cpu().numpy()+1)/2
            rgb=(cv_img*255).astype(np.uint8)
            bgr=cv2.cvtColor(rgb,cv2.COLOR_RGB2BGR)
            cv2.imwrite(sub_path+'/'+str(step)+'.jpg',bgr)
        
        step += 1
        if epoch_iter >= dataset_size:
            break
