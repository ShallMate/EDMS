# EDMS

**main.py** is the example of key generation, BuildindexTree, SearchIndex, Insert and Delete algorithms.
<br /> **EDMS.py** is the algorithms of EDMS, which contain BuildindexTree, SearchIndex, Insert and Delete algorithms
<br /> **key_deal.py** is an object that generates the secret key.
<br /> **attribute_tree.py** is the object of age attribute hierarchy structure. 
<br /> **num_tree.py** is the object of number attribute hierarchy structure. 
<br /> **Update.py** is the object of number attribute hierarchy structure.
<br /> **pre_tree.py** is the object of plaintext index tree.

<br /> The source code requires Pandas library for CSV file reading.

<br /> The dataset of our experiment is from ''Impact of HbA1c Measurement on Hospital Readmission Rates:
Analysis of 70,000 Clinical Database Patient Records'', which contains 100000 medical records of diabetes
patients, including medical card number, gender, age, treatment and other private information.

<br /> For documents in '.\doc\dia-100k', there are the dateset from 10000 EHRs to 100000 EHRs when the number
of keywords is fixed as 4000.
<br /> For documents in '.\doc\keyword-4000', there are the dateset from 2000 EHRs to 8000 EHRs when the number
of keywords is fixed as 4000. The dataset of this document is used for experimental comparison with EDMRS and MRSE.
<br /> For documents in '.\doc\storage', there are the dateset from 1000 keywords to 5000 keywords when the number
of EHRs is fixed as 1000. The dataset of this document is used for experimental comparison with the storage overhead of 
EDMRS.
<br /> For documents in '.\doc\enfile', there are the encrypted EHRs.
<br /> For documents in '.\doc\index', there are the indexes of dataset from storage document.
<br /> medical.csv is the EHRs that meet the search criteria and are decrypted.
<br /> The result:
<br />Buildindex: 11.5504468 seconds  --the time cost to build encrypted index tree
<br />Trapdoor: 0.002020599999999817 seconds --the time cost to generate a trapdoor
<br />Search: 0.01348579999999977 seconds --the time cost to search
<br />[966, 2933, 8473, 9180, 6540, 5741, 8031, 
2456, 4546, 6889, 1042, 3252, 7918, 401, 6223, 9454] --the search result
<br />Insert: 0.0026684000000010144 seconds --the time cost of the insert operation
<br />[100240] --vertify the insert operation.
<br />Delete: 0.08664469999999902 seconds --the time cost of the delete operation
<br />[] --vertify the delete operation.