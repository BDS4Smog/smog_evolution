function [ accuracy ] = ELM_K( type, name, k )
%EVALUATION_ELM2 Summary of this function goes here
%   Detailed explanation goes hert

type = 'station';
name = 'Dongsi';
k = 1;

LABEL_NUM=6;
NEURONS =[6,6,6,6,6,2];

tr_FILE = strcat(name,'_key1/',type,'_',name,'.txt');
tr_data = load(tr_FILE);
te_data = tr_data(find(tr_data(:,12)==0),:);
tr_data = tr_data(find(tr_data(:,12)==1),:);
tr_data = [tr_data(:,11) tr_data(:,8) tr_data(:,9:10)];
te_data = [te_data(:,11) te_data(:,8) te_data(:,9:10)];
TrAccuracy=0;
TeAccuracy=0;
for i = 1:50

    [TrainingAccuracy, TestingAccuracy] = my_ELM(tr_data,te_data, 1,50 , 'sig');
    TrAccuracy=TrAccuracy+TrainingAccuracy;
    TeAccuracy=TrAccuracy+TestingAccuracy;
end
TrAccuracy=TrAccuracy/50;
TeAccuracy=TeAccuracy/50






end




