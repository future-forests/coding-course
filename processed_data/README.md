### Course exercise data (if you miss class 1)

During the first class, we will download the data we will use throughout the course together. If you were unable to attend the first class, here is what you need to do.

#### a. If you have access to uc3

**From uc3 (Class 1):** copy shared course data to your machine.

```bash
mkdir -p processed_data
scp -r YOUR_USERNAME@uc3.scc.kit.edu:/path/to/coding-course/exercises/ processed_data/
```

Replace `YOUR_USERNAME` with your bwUniCluster username (e.g. `fr_ab1234`). You need to be on the **Uni-Freiburg network or VPN** for uc3.

#### b. If you don't have access to uc3

Copy the folder `processed_data` from our shared drive, to your working directly:

```
un042rd01/01_General/02_Central_infrastructure/SES_ModelLab/coding-course/
```

### Class 5b survey data (DIANA)

`diana_owners.csv`, `diana_codebook.csv` and `diana_text_labels.csv` are a **modified teaching version** of the DIANA forest-owner survey (University of Freiburg, 2025). Rows no longer correspond to real people: answers were swapped between similar respondents and slightly perturbed. Use these files only for the course: do not share, cite or use them for research. For the real data, contact the DIANA team.
