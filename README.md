# MIRACLE

MIRACLE (Microsatellite Instability detection with RNA-seq by Analyzing Comparison of Length Extensively) is a tool designed for detecting microsatellite instability (MSI) using RNA-seq data by comparing length variation. The steps of MIRACLE consist of three parts.
* In the first step, it measures the length of microsatellites in the tumor sample BAM file inputted.
* In the second step, it conducts statistical analysis to compare the length distribution of microsatellites and measure the extent of MSI events that have occurred.
* In the third step, it calculates the probability of the sample being MSI-H or MSS using the measured MSI events.

---

## Authors
  * Jin-Wook Choi (argon502@snu.ac.kr)
  * Jin-Ok Lee (xuanhaoyang@stu.xjtu.edu.cn)
  * Sejoon Lee (sejoonlee@snubh.org)
 
 ---
## License

---
## How to use MIRACLE?

### Install with pip3   
  ```shell script
    conda create -n myenv python>=3.6
    conda activate myenv
    git clone https://github.com/xjtu-omics/msisensor-rna.git
    pip3 install .
  ```
### Usage:   
   ```shell script
    MIRACLE <command> [options]
```
### Options:
  ```
    * Required arguments
    -i 
  ```
---
## Input and output

  * The input file for informative genes selection and model training. (-i option in train command)
  
       You need to prepare your training file with a comma separated format (csv). 
       The first columns should be sample id, the second columns should be msi status, 
       and the third and other columns should be gene expression values. We recommend 
       you provide a normalized expression values. (like z-score normalization with log2(FPKM+1) )
       
       The following is an example:
       
    |  SampleID   | msi  | MLH1|LINC01006| ...| NHLRC1|
    |  ----  | ----  | ---- | ----|  ---- | ----|
    | NA0001  | MSI-H | 0.209|1.209|...|0.393|
    | CA0002  | MSS |5.690|0.620|...|4.902|
    | ...  | ... |...|...|...|...|
    | CA10 0  | MSS |9.960|0.920|...|5.002|
  * The trained model (-m option in train, show and detection command)
  
    The trained model is saved as pickle file. In train command, we recommend you add more 
    description by -di,-dm,-a,-e, so that others who used this model are able to get more information.
    In show command, you can get the information of your model , and changed some descriptions by -di and  -dm.
    you can also use -g option to output the genes list this model needed to a file. 
    In detection command, you must check the model and input Yes or No to continue the predict step use *-d True* 
    to ignore this reminder.      
  
  
   
  * The input file for the detection command (-i option in detection command)    
  
      You need to prepare your input file for MSI prediction with a comma separated format (csv). 
       The first columns should be sample id, the second and other columns should be gene expression values.
       The genes name must contain the genes in the model (use -g option of show command to see the genes 
       list of the model).  
       The following is an example:
       
    |  SampleID   | MLH1|LINC01006| ...| NHLRC1|
    |  ----  | ---- | ----|  ---- | ----|
    | NA0001|  0.209|1.209|...|0.393|
    | CA0002 |5.690|0.620|...|4.902|
    | ...   |...|...|...|...|
    | CA100|9.960|0.920|...|5.002|
  
---

## Contact

If you have any questions, please contact with Jin-Wook Choi (argon502@snu.ac.kr).
