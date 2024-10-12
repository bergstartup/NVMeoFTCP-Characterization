REMOTE=nvme3n1
LOCAL=nvme0c0n1
SCHED=$1

#Change the target I/O scheduler to none
curl "http://172.16.137.2:8080/sched?sched=none&dev=${REMOTE}"

#Change local scheduler to none
curl "http://localhost:8080/sched?sched=none&dev=${LOCAL}"
python3 fio_runner.py remote_lhead_intra_none
python3 fio_runner.py remote_lhead_inter_nopin_none
python3 fio_runner.py remote_lhead_inter_none
python3 fio_runner.py remote_thead_none


#Change local scheduler to kyber
curl "http://localhost:8080/sched?sched=${SCHED}&dev=${LOCAL}"
python3 fio_runner.py remote_lhead_intra_none
python3 fio_runner.py remote_lhead_intra_i${SCHED}
python3 fio_runner.py remote_lhead_inter_nopin_i${SCHED}
python3 fio_runner.py remote_lhead_inter_i${SCHED}
python3 fio_runner.py remote_thead_i${SCHED}



#Change the target I/O scheduler to kyber
curl "http://172.16.137.2:8080/sched?sched=${SCHED}&dev=${REMOTE}"

#Change local scheduler to none
curl "http://localhost:8080/sched?sched=none&dev=${LOCAL}"
python3 fio_runner.py remote_lhead_intra_t${SCHED}
python3 fio_runner.py remote_lhead_inter_nopin_t${SCHED}
python3 fio_runner.py remote_lhead_inter_t${SCHED}
python3 fio_runner.py remote_thead_t${SCHED}

#Change local scheduler to kyber
curl "http://localhost:8080/sched?sched=${SCHED}&dev=nvme4c4n1"
python3 fio_runner.py remote_lhead_intra_it${SCHED}
python3 fio_runner.py remote_lhead_inter_nopin_it${SCHED}
python3 fio_runner.py remote_lhead_inter_it${SCHED}
python3 fio_runner.py remote_thead_it${SCHED}
