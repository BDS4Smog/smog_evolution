function [ accuracy ] = ELM_K( type, name, k,if_pca)
%EVALUATION_ELM2 Summary of this function goes here
%   Detailed explanation goes hert

type = 'station';
name = 'Dongsi';
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
    if if_pca == 1
        [COEFF,tr_SCORE,LATENT] = princomp(tr_data(:,3:32));
        tr_data_used = [tr_data(:,34) tr_SCORE(:,1:REDUCED_DIM)]; 
    else
        tr_data_used = [tr_data(:,34) tr_data(:,3:32)];
    end 
    
    [TrainingAccuracy]=my_elm_train(tr_data_used,1,NEURONS(i),'sig',['model',num2str(i)]);
end

te_FILE = strcat(name,'_key',num2str(k),'/',type, '_', name,'.txt');    
te_data = load(te_FILE);
te_data = te_data(find(te_data(:,35)==0),:);

N = size(te_data,1);
correct = 0;
result = zeros(N,LABEL_NUM);
result2 = zeros(N,3);
for i = 1:N
    M = [];
    for j = 1:LABEL_NUM
       if if_pca == 1
           te_SCORE = te_data(i,3:32)*COEFF;
           te_data_used = [te_data(i,34) te_SCORE(:,1:REDUCED_DIM)];
       else
           te_data_used = [te_data(i,34) te_data(i,3:32)];
       end
       
       [tmp_output,label] = my_elm_predict(te_data_used,['model',num2str(j)]);
       
       tmp_output = (tmp_output-min(tmp_output))/(max(tmp_output)-min(tmp_output));
       tmp_output = tmp_output/sum(tmp_output);
       
       tmp = zeros(1,LABEL_NUM);
       tmp(1,label)=tmp_output;
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
    [tmp ,c]=max(result(i,:));
    result2(i,1)=te_data(i,33);
    result2(i,2)=te_data(i,34);
    result2(i,3)=c;
    if c==te_data(i,34)
        correct = correct+1;
    end
end

accuracy = correct/N;



for i = 1:LABEL_NUM
    delete(['model',num2str(i),'.mat']);
end
end




