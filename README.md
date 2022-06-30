## RMGN-VITON

![example image](./examples/example.png)

> **RMGN: A Regional Mask Guided Network for Parser-free Virtual Try-on**<br>
> In IJCAI-ECAI 2022(short oral).

>[[Paper]](http://arxiv.org/abs/2204.11258)
>[[Supplementary Material]](https://drive.google.com/file/d/1Io5VODelB3J8tXznATQQWlaKiR_xycg-/view?usp=sharing)

> **Abstract:** *Virtual try-on(VTON) aims at fitting target clothes to reference person images, which is widely adopted in e-commerce.Existing VTON approaches can be narrowly categorized into Parser-Based(PB) and Parser-Free(PF) by whether relying on the parser information to mask the persons' clothes and synthesize try-on images. Although abandoning parser information has improved the applicability of PF methods, the ability of detail synthesizing has also been sacrificed. As a result, the distraction from original cloth may persistin synthesized images, especially in complicated postures and high resolution applications. To address the aforementioned issue, we propose a novel PF method named Regional Mask Guided Network(RMGN). More specifically, a regional mask is proposed to explicitly fuse the features of target clothes and reference persons so that the persisted distraction can be eliminated. A posture awareness loss and a multi-level feature extractor are further proposed to handle the complicated postures and synthesize high resolution images. Extensive experiments demonstrate that our proposed RMGN outperforms both state-of-the-art PB and PF methods.Ablation studies further verify the effectiveness ofmodules in RMGN.*


## Test Results

We achieves FID 9.93 on VITON test set (512x384) with the [[test_pairs.txt]](https://drive.google.com/file/d/15syEhwteKep_EBf7SWSIKGwKDEuw1AYC/view?usp=sharing). The test results is here[[test reults]](https://drive.google.com/file/d/1LIQihyE_VXQFEt0IEuw3_BOdlQaKs_9B/view?usp=sharing)

## Citation

If you find this work useful for your research, please cite our paper:

```
@inproceedings{lin2022viton,
  title={RMGN: A Regional Mask Guided Network for Parser-free Virtual Try-on},
  author={Lin, Chao and Li, Zhao and Zhou, Sheng and Hu, Shichang and Zhang, Jialun and Luo, Linhao and Zhang, Jiarun and Huang, Longtao and He, Yuan},
  booktitle={IJCAI},
  year={2022}
}
```
