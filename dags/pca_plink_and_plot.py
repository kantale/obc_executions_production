
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'Airflow',
    'start_date': datetime(2015, 6, 1),
}


dag = DAG(
    'pca_plink_and_plot__1', default_args=default_args, schedule_interval=None)


plink__1_90beta_20190617__1 = BashOperator(
    
    task_id='plink__1_90beta_20190617__1',
    bash_command="""
### BASH INSTALLATION COMMANDS FOR TOOL: plink/1.90beta_20190617/1
echo "OBC: INSTALLING TOOL: plink/1.90beta_20190617/1"
(
# Insert the BASH commands that install this tool
# The following tools are available:
#  apt-get, wget

./plink --file toy
if [ $? -ne 0 ] ; then
 wget http://s3.amazonaws.com/plink1-assets/plink_linux_x86_64_20190617.zip
 unzip plink_linux_x86_64_20190617.zip
fi


)
echo "OBC: INSTALLATION OF TOOL: plink/1.90beta_20190617/1 . COMPLETED"
### END OF INSTALLATION COMMANDS FOR TOOL: plink/1.90beta_20190617/1

### BASH VALIDATION COMMANDS FOR TOOL: plink/1.90beta_20190617/1
echo "OBC: VALIDATING THE INSTALLATION OF THE TOOL: plink/1.90beta_20190617/1"
(
# Insert the BASH commands that confirm that this tool is correctly installed
# In success, this script should return 0 exit code.
# A non-zero exit code, means failure to validate installation.

./plink --file toy

)
if [ $? -eq 0 ] ; then
   echo "OBC: VALIDATION FOR TOOL: plink/1.90beta_20190617/1 SUCCEEDED"
else
   echo "OBC: VALIDATION FOR TOOL: plink/1.90beta_20190617/1 FAILED"
fi

### END OF VALIDATION COMMANDS FOR TOOL: plink/1.90beta_20190617/1

### SETTING TOOL VARIABLES FOR: plink/1.90beta_20190617/1
export plink__1_90beta_20190617__1__path="./plink" # installation path of executable 
echo "OBC: SET plink__1_90beta_20190617__1__path=$plink__1_90beta_20190617__1__path   <-- installation path of executable "
### END OF SETTING TOOL VARIABLES FOR: plink/1.90beta_20190617/1

### CREATING BASH WITH TOOL VARIABLES
cat > ${OBC_WORK_PATH}/plink__1_90beta_20190617__1_VARS.sh << ENDOFFILE
plink__1_90beta_20190617__1__path="./plink"
ENDOFFILE

""",
    dag=dag)


anaconda3__2019_03__1 = BashOperator(
    
    task_id='anaconda3__2019_03__1',
    bash_command="""
### BASH INSTALLATION COMMANDS FOR TOOL: anaconda3/2019.03/1
echo "OBC: INSTALLING TOOL: anaconda3/2019.03/1"
### READING VARIABLES FROM ${OBC_WORK_PATH}/plink__1_90beta_20190617__1_VARS.sh
. ${OBC_WORK_PATH}/plink__1_90beta_20190617__1_VARS.sh

(
# Insert the BASH commands that install this tool
# The following tools are available:
#  apt-get, wget

md5sum  Anaconda3-2019.03-Linux-x86_64.sh | grep 43caea3d726779843f130a7fb2d380a2
if [ $? -ne 0 ]; then
   wget https://repo.anaconda.com/archive/Anaconda3-2019.03-Linux-x86_64.sh 
   bash Anaconda3-2019.03-Linux-x86_64.sh -b -p ./anaconda3
fi

)
echo "OBC: INSTALLATION OF TOOL: anaconda3/2019.03/1 . COMPLETED"
### END OF INSTALLATION COMMANDS FOR TOOL: anaconda3/2019.03/1

### BASH VALIDATION COMMANDS FOR TOOL: anaconda3/2019.03/1
echo "OBC: VALIDATING THE INSTALLATION OF THE TOOL: anaconda3/2019.03/1"
(
# Insert the BASH commands that confirm that this tool is correctly installed
# In success, this script should return 0 exit code.
# A non-zero exit code, means failure to validate installation.

md5sum  Anaconda3-2019.03-Linux-x86_64.sh | grep 43caea3d726779843f130a7fb2d380a2
if [ $? -ne 0 ]; then
   exit 1
fi

./anaconda3/bin/python --version
if [ $? -ne 0 ]; then
   exit 1
fi

exit 0


)
if [ $? -eq 0 ] ; then
   echo "OBC: VALIDATION FOR TOOL: anaconda3/2019.03/1 SUCCEEDED"
else
   echo "OBC: VALIDATION FOR TOOL: anaconda3/2019.03/1 FAILED"
fi

### END OF VALIDATION COMMANDS FOR TOOL: anaconda3/2019.03/1

### SETTING TOOL VARIABLES FOR: anaconda3/2019.03/1
export anaconda3__2019_03__1__path="./anaconda3/bin/python" # Installation python 
echo "OBC: SET anaconda3__2019_03__1__path=$anaconda3__2019_03__1__path   <-- Installation python "
### END OF SETTING TOOL VARIABLES FOR: anaconda3/2019.03/1

### CREATING BASH WITH TOOL VARIABLES
cat > ${OBC_WORK_PATH}/anaconda3__2019_03__1_VARS.sh << ENDOFFILE
anaconda3__2019_03__1__path="./anaconda3/bin/python"
ENDOFFILE

""",
    dag=dag)


step__main_step__pca_plink_and_plot__1 = BashOperator(
    
    task_id='step__main_step__pca_plink_and_plot__1',
    bash_command="""
. ${OBC_WORK_PATH}/plink__1_90beta_20190617__1_VARS.sh
. ${OBC_WORK_PATH}/anaconda3__2019_03__1_VARS.sh
OBC_START=$(eval "declare")
# Insert the BASH commands for this step

input__pedmap__pca_plink__1=${input__pedmap__pca_plink_and_plot__1}

OBC_CURRENT=$(eval "declare")
comm -3 <(echo "$OBC_START" | grep -v "_=") <(echo "$OBC_CURRENT" | grep -v OBC_START | grep -v PIPESTATUS | grep -v "_=") > ${OBC_WORK_PATH}/step__main_step__pca_plink_and_plot__1__1.sh

""",
    dag=dag)


step__main_step__pca_plink__1 = BashOperator(
    
    task_id='step__main_step__pca_plink__1',
    bash_command="""
. ${OBC_WORK_PATH}/plink__1_90beta_20190617__1_VARS.sh
. ${OBC_WORK_PATH}/anaconda3__2019_03__1_VARS.sh
. ${OBC_WORK_PATH}/step__main_step__pca_plink_and_plot__1__1.sh
OBC_START=$(eval "declare")
# Insert the BASH commands for this step

output__result_pca__pca_plink__1=${input__pedmap__pca_plink__1}_pca

${plink__1_90beta_20190617__1__path}    --file ${input__pedmap__pca_plink__1}    --pca    --out ${output__result_pca__pca_plink__1}
   

   
OBC_CURRENT=$(eval "declare")
comm -3 <(echo "$OBC_START" | grep -v "_=") <(echo "$OBC_CURRENT" | grep -v OBC_START | grep -v PIPESTATUS | grep -v "_=") > ${OBC_WORK_PATH}/step__main_step__pca_plink__1__1.sh

""",
    dag=dag)


step__main_step__pca_plink_and_plot__1 = BashOperator(
    
    task_id='step__main_step__pca_plink_and_plot__1',
    bash_command="""
. ${OBC_WORK_PATH}/plink__1_90beta_20190617__1_VARS.sh
. ${OBC_WORK_PATH}/anaconda3__2019_03__1_VARS.sh
. ${OBC_WORK_PATH}/step__main_step__pca_plink_and_plot__1__1.sh
. ${OBC_WORK_PATH}/step__main_step__pca_plink__1__1.sh
OBC_START=$(eval "declare")


input__eigenvectors__2d_scatter_of_plink_pca__1=${output__result_pca__pca_plink__1}.eigenvec

OBC_CURRENT=$(eval "declare")
comm -3 <(echo "$OBC_START" | grep -v "_=") <(echo "$OBC_CURRENT" | grep -v OBC_START | grep -v PIPESTATUS | grep -v "_=") > ${OBC_WORK_PATH}/step__main_step__pca_plink_and_plot__1__2.sh

""",
    dag=dag)


step__main_step__2d_scatter_of_plink_pca__1 = BashOperator(
    
    task_id='step__main_step__2d_scatter_of_plink_pca__1',
    bash_command="""
. ${OBC_WORK_PATH}/plink__1_90beta_20190617__1_VARS.sh
. ${OBC_WORK_PATH}/anaconda3__2019_03__1_VARS.sh
. ${OBC_WORK_PATH}/step__main_step__pca_plink_and_plot__1__1.sh
. ${OBC_WORK_PATH}/step__main_step__pca_plink__1__1.sh
. ${OBC_WORK_PATH}/step__main_step__pca_plink_and_plot__1__2.sh
OBC_START=$(eval "declare")
# Insert the BASH commands for this step

cat > p.py << EOFF

import pandas as pd

fn = "${input__eigenvectors__2d_scatter_of_plink_pca__1}"
df = pd.read_csv(fn, header=None, sep=' ')
ax = df.plot.scatter(x=2, y=3)
fig = ax.figure
fig.savefig('scatter_plot.pdf')

EOFF

${anaconda3__2019_03__1__path} p.py

output__plot__2d_scatter_of_plink_pca__1=scatter_plot.pdf

OBC_CURRENT=$(eval "declare")
comm -3 <(echo "$OBC_START" | grep -v "_=") <(echo "$OBC_CURRENT" | grep -v OBC_START | grep -v PIPESTATUS | grep -v "_=") > ${OBC_WORK_PATH}/step__main_step__2d_scatter_of_plink_pca__1__1.sh

""",
    dag=dag)


step__main_step__pca_plink_and_plot__1 = BashOperator(
    
    task_id='step__main_step__pca_plink_and_plot__1',
    bash_command="""
. ${OBC_WORK_PATH}/plink__1_90beta_20190617__1_VARS.sh
. ${OBC_WORK_PATH}/anaconda3__2019_03__1_VARS.sh
. ${OBC_WORK_PATH}/step__main_step__pca_plink_and_plot__1__1.sh
. ${OBC_WORK_PATH}/step__main_step__pca_plink__1__1.sh
. ${OBC_WORK_PATH}/step__main_step__pca_plink_and_plot__1__2.sh
. ${OBC_WORK_PATH}/step__main_step__2d_scatter_of_plink_pca__1__1.sh
OBC_START=$(eval "declare")


output__plot__pca_plink_and_plot__1=${output__plot__2d_scatter_of_plink_pca__1}


OBC_CURRENT=$(eval "declare")
comm -3 <(echo "$OBC_START" | grep -v "_=") <(echo "$OBC_CURRENT" | grep -v OBC_START | grep -v PIPESTATUS | grep -v "_=") > ${OBC_WORK_PATH}/step__main_step__pca_plink_and_plot__1__3.sh

""",
    dag=dag)


plink__1_90beta_20190617__1 >> anaconda3__2019_03__1 >> step__main_step__pca_plink_and_plot__1 >> step__main_step__pca_plink__1 >> step__main_step__pca_plink_and_plot__1 >> step__main_step__2d_scatter_of_plink_pca__1 >> step__main_step__pca_plink_and_plot__1
