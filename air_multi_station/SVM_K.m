function [ accuracy ] = ELM_K( type, name, k,if_pca)
%EVALUATION_ELM2 Summary of this function goes here
%   Detailed explanation goes hert

type = 'station';
name = 'Haidian';
k=1;
if_pca = 0;

LABEL_NUM=6;
NEURONS =[30,20,20,10,10,5];
REDUCED_DIM = 15;

for i = 1:LABEL_NUM
    
	tr_FILE = strcat(name,'_key1/',type,'_',name,'_',num2str(i),'.txt');
    tr_data = load(tr_FILE);
    
    tr_data = tr_data(find(tr_data(:,35)==1),:);
%   tr_data = [tr_data(:,34) tr_data(:,3) tr_data(:,9) tr_data(:,15) tr_data(:,21) tr_data(:,27)]

    
    model(i)=svmtrain(tr_data(:,34),tr_data(:,3:32),'-b 1');
end

te_FILE = strcat(name,'_key',num2str(k),'/',type, '_', name,'.txt');    
te_data = load(te_FILE);
te_data = te_data(find(te_data(:,35)==0),:);

N = size(te_data,1);
correct = 0;
result = zeros(N,LABEL_NUM);
for i = 1:N
    M = [];
    for j = 1:LABEL_NUM
       
       label = model(j).Label;
       [~,~,tmp_output] = svmpredict(te_data(i,34),te_data(i,3:32),model(j),'-b 1');
       

       
       tmp = zeros(1,LABEL_NUM);
       tmp(1,label')=tmp_output;
       M = [M;tmp];
    end
    init = zeros(1,LABEL_NUM);
    init(1,te_data(i,33)) = 1;
    if k==1
        result(i,:) = init*M;
    end
    if k==2
        result(i,:) = init*M*M;
    end
    [ tmp ,c]=max(result(i,:));
    if c==te_data(i,34)
        correct = correct+1;
    end
end

accuracy = correct/N;

for i = 1:LABEL_NUM
    delete(['model',num2str(i),'.mat']);
end
end




