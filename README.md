# MIRACLEpy

MIRACLE (Microsatellite Instability detection with RNA-seq by Analyzing Comparison of Length Extensively) is a tool designed for detecting microsatellite instability (MSI) using RNA-seq data by comparing length variation. The steps of MIRACLE consist of three parts.
* In the first step, it measures the length of microsatellites in the tumor sample BAM file inputted.
* In the second step, it conducts statistical analysis to compare the length distribution of microsatellites and measure the extent of MSI events that have occurred.
* In the third step, it calculates the probability of the sample being MSI-H or MSS using the measured MSI events.

---

## Authors
  * Jin-Wook Choi (argon502@snu.ac.kr)
  * Jin-Ok Lee (jinoklee.01@gmail.com)
  * Sejoon Lee (sejoonlee@snubh.org)
 
 ---
## License

---
## How to use MIRACLE?

### Install with pip3   
  ```shell script
    pip install --index-url https://test.pypi.org/simple/ MIRACLE
  ```
### Usage:   
   ```shell script
    MIRACLE -i INPUT -o OUTPUT [options]
```
### Options:
  ```
-i, --input INPUT                     :Input bam file [required]

-o, --output OUTPUT                   :Output file name [required]

-b, --bed BED                         :Information of microsatellite in bed format [default: Reference_MS.bed]

-m, --minimum MINIMUM_LENGTH          :Minimum length for microsatellite [default: 5]

-f, --flanking FLANKING_LENGTH        :Flanking region length for matching microsatellite [default :2]

-F, --FDR FDR_THRESHOLD               :FDR value for significance [default :0.05]

-r, --read MINIMUM_READ_COUNT         :Minimum read count of matched microsatellite [default :6]

-n, --normal MATCHED_NORMAL           :Matched normal bam file of INPUT [default :Reference_normal]

-R, --Random RATIO_OF_RANDOM_SAMPLING :Ratio of training set for random sampling [default :0.8]

-M, --Model TRAINING_DATA_SET         :Training data set for making model [default :Traning_data_set]

  ```
---
## Input file

  * The input file for microsatellite reference set. (-b option)
    
    You need to prepare microsatellite set that you want to investigate.
    Or, you can use the reference microsatellite set in manual.
    All of microsatellite information should be prepared with bed format.

    The first columns should be chromosome number, the second and third columns should be start and end of microsatellitemsi status, respectively.
    The fourth coloumn should be the gene name which cover the microsatellite.
    The fifth coloumn should be the type of repeat (mono, di, tri, tetra).
    The sixth coloumn should be the sequence of microsatellite with five flanking base pair.
       
    The following is an example:
       
    |Chr number|MS Start|MS End|Gene name|Repeat type|Sequence|
    |  ----  | ----  | ---- | ----|  ---- | ----|
    | chr1  | 14488 | 14493 |WASH7P|mono|GCCGTCCCCCCATGGA|
    | chr1  | 14670 | 14676 |WASH7P|mono|GGTCTGGGGGGGAAGGT|
    | chr1  | 14717 | 14724 |WASH7P|tri|CCTCGTCCTCCTCTGCCT|
    | chr1  | 14733 | 14740 |WASH7P|tri|CTGTGGCTGCTGCGGTGG|


  * The training data (-M option)
  
    The training data is served as tsv file with three column.
    The first column should contain the name of case.
    The second column should contain MSS status of the case.
    The third column should contain the number of unstable microsatellites.
 
---

## Contact

If you have any questions, please contact with Jin-Wook Choi (argon502@snu.ac.kr).
