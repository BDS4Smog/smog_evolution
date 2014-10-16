function [ Train_Accuracy,Test_Accuracy ] = evaluate_ELM( type,station )
%EVALUATE_ELM Summary of this function goes here
%   Detailed explanation goes here
%Local air
%station = 'haidian';
%type = 2;
if type==0
    range=2:7;
end
if type==1
    range=8:14;
end

if type==2
    range = 14;
end

ROUND_NUM = 4;

d0 = load(['data/' station '_low.txt']);
d0 = [zeros(size(d0,1),1) d0(:,range)];
d1 = load(['data/' station '_increase.txt']);
d1 = [ones(size(d1,1),1) d1(:,range)];
d = [d0' d1']';
d = d(randperm(length(d)),:); 
Train_Accuracy = 0;
Test_Accuracy = 0;
for i = 1:ROUND_NUM
    start_1 = 1+(i-1)*floor(length(d)/ROUND_NUM);
    end_1 = i*floor(length(d)/ROUND_NUM); 
    Te = d(start_1:end_1,:);
    if i == 1
        Tr = d(end_1+1:length(d),:);
    elseif i == ROUND_NUM
        Tr = d(1:start_1-1,:);
    else
        Tr = [d(1:start_1-1,:)',d(end_1+1:length(d),:)']';    
    end
    [Tr_acc, Te_acc] = my_ELM(Tr, Te, 1, 30, 'sig');
    Train_Accuracy = Train_Accuracy + Tr_acc;
    Test_Accuracy = Test_Accuracy + Te_acc;
end
Train_Accuracy = Train_Accuracy/ROUND_NUM;
Test_Accuracy = Test_Accuracy/ROUND_NUM;

end

