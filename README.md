# capstone_prj_g9

Project Proposal document- https://docs.google.com/document/d/1T8IhLUb-7LoIuGSndTh8mr4WoNfkXhRNV3fpCu05zuc/edit?usp=sharing

Colab Notebooks- 1) part-1: audio summarization- https://colab.research.google.com/drive/1wxb1a1wlSGu4UjK8-nLTVizv2SpGB_pH?usp=sharing

2) part-2-: audio to ai avatar gen-  https://colab.research.google.com/drive/1B1jiEC_nyZDSo-vbYVnTmA_pMvEdfAzo?usp=sharing


Build:

1. sudo docker build -t resume_video .
2. sudo docker run -d -p 8000:8000 -p 7680:7680 resume_video
3. sudo docker run -d   -p 9090:9090   -v $(pwd)/Prometheus/prometheus.yml:/etc/prometheus/prometheus.yml   prom/prometheus
4. sudo docker run -d   -p 3000:3000   --name=grafana   grafana/grafana
