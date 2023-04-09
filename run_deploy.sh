until [[ -f 'job_completed.txt']]
source /home/ubuntu/mambaforge/bin/activate /home/ubuntu/mambaforge/envs/socials \
 && conda activate socials && \
 python /home/ubuntu/programowanie/mecz/deploy_fromFixtures.py >> /tmp/deploy_log.log

