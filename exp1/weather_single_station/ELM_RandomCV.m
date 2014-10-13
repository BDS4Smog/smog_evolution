function [ Train_acc, Test_acc ] = ELM_RandomCV( type,name )
%CALCULATEM_ELM Summary of this function goes here
%   Detailed explanation goes here
type = 'station'
name = 'Dongsi'
LABEL_NUM=6;
ROUND_NUM=4;
NEURONS =[10,10,8,8,5,5];
Train_acc = [0,0,0,0];
Test_acc = [0,0,0,0];
for j = 1:LABEL_NUM
    FILE = strcat(name,'_key1/',type,'_',name,'_',num2str(j),'.txt');
    tmp = load(FILE);
    T=tmp(randperm(length(tmp)),:);  
    for i = 1:ROUND_NUM      
       start_1 = 1+(i-1)*floor(length(T)/ROUND_NUM);
       end_1 = i*floor(length(T)/ROUND_NUM);
       Te = T(start_1:end_1,:);
       Te = [Te(:,11),Te(:,3:9)];
       if i == 1
           Tr = T(end_1+1:length(T),:);
       elseif i == ROUND_NUM
           Tr = T(1:start_1-1,:);
       else
           Tr = [T(1:start_1-1,:)',T(end_1+1:length(T),:)']';    
       end
       Tr = [Tr(:,11),Tr(:,3:9)];
       [Tr_acc, Te_acc] = my_ELM(Tr, Te, 1, NEURONS(j), 'sig')
       Train_acc(i) = Train_acc(i) + Tr_acc;
       Test_acc(i) = Test_acc(i) + Te_acc;
   end
end
Train_acc=Train_acc./LABEL_NUM;
Test_acc=Test_acc./LABEL_NUM;
end

