FROM tensorflow/tensorflow:0.9.0-devel

MAINTAINER Jerome WAX "xblaster@lo2k.net"

WORKDIR /tensorflow

ADD src .

RUN git pull
CMD cd /tensorflow && ./train.sh
RUN mkdir /tf_files
RUN cp  /tensorflow/tensorflow/examples/image_retraining/retrain.py /tf_files
RUN cp -avr /tensorflow/zvonimir_detection/data /tf_files
RUN cp -avr /tensorflow/zvonimir_detection/test-vrata /tf_files
