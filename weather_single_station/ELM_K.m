function [ accuracy ] = evaluation_ELM_key2( type, name )
%EVALUATION_ELM2 Summary of this function goes here
%   Detailed explanation goes hert

type = 'station'
name = 'Dongsi'

LABEL_NUM=6;
NEURONS =[6,6,6,6,6,2];

for i = 1:LABEL_NUM
    
	tr_FILE = strcat(name,'_key1/',type,'_',name,'_',num2str(i),'.txt');
    tr_data = load(tr_FILE);
    
    tr_data = tr_data(find(tr_data(:,12)==1),:);
    n=size(tr_data,1);
    tr_data(:,3:9)=(tr_data(:,3:9)-ones(n,1)*min(tr_data(:,3:9)))./(ones(n,1)*(max(tr_data(:,3:9))-min(tr_data(:,3:9))));
    
    tr_data = [tr_data(:,11) tr_data(:,3:9)];
    
    
    my_elm_train(tr_data,1,NEURONS(i),'sig',['model',num2str(i)]);
end

te_FILE = strcat(name,'_key1/',type, '_', name,'.txt');    
te_data = load(te_FILE);
te_data = te_data(find(te_data(:,12)==0),:);

N = size(te_data,1);
correct = 0;
result = zeros(N,LABEL_NUM);
for i = 1:N
    M = [];
    for j = 1:LABEL_NUM
       [tmp_output,label] = my_elm_predict([te_data(i,11) te_data(i,3:9)],['model',num2str(j)]);
       
       tmp_output = (tmp_output-min(tmp_output))/(max(tmp_output)-min(tmp_output));
       tmp_output = tmp_output/sum(tmp_output);
       
       tmp = zeros(1,LABEL_NUM);
       tmp(1,label)=tmp_output;
       M = [M;tmp];
    end
    init = zeros(1,LABEL_NUM);
    init(1,te_data(i,10)) = 1;
    
    result(i,:) = init*M;
    [ tmp ,c]=max(result(i,:));
    if c==te_data(i,11)
        correct = correct+1;
    end
end

accuracy = correct/N;
for i = 1:LABEL_NUM
    delete(['model',num2str(i),'.mat']);
end
end




