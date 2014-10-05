function evaluation_ELM( type,name )
%CALCULATEM_ELM Summary of this function goes here
%   Detailed explanation goes here
LABEL_NUM=6;
ROUND_NUM=4;
NEURONS =[20,20,20,20,20,5];
for j = 1:LABEL_NUM
    FILE = strcat(name,'_key1/',type,'_',name,'_',num2str(j),'.txt');
    tmp = load(FILE);
    T=tmp(randperm(length(tmp)),:);  
    for i = 1:ROUND_NUM      
       start_1 = 1+(i-1)*floor(length(T)/ROUND_NUM);
       end_1 = i*floor(length(T)/ROUND_NUM);
       Te = T(start_1:end_1,:);
       Te = [Te(:,10),Te(:,3:8)];
       if i == 1
           Tr = T(end_1+1:length(T),:);
       elseif i == ROUND_NUM
           Tr = T(1:start_1-1,:);
       else
           Tr = [T(1:start_1-1,:)',T(end_1+1:length(T),:)']';    
       end
       Tr = [Tr(:,10),Tr(:,3:8)];
       [Tr_acc, Te_acc] = my_ELM(Tr, Te, 1, NEURONS(j), 'sig');
       fprintf('Level: %d, Round: %d, Training Acc: %4.4f, Testing Acc: %4.4f \n', j, i, Tr_acc, Te_acc); 
   end
end
end

