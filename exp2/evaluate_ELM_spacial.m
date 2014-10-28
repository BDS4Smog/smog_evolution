function evaluate_ELM( range,station )
%EVALUATE_ELM Summary of this function goes here
%   Detailed explanation goes here
%Local air
station = 'haidian';
range = [3:7];

f1 = ['data_spacial/' station '_increase_6h.txt'];
f0 = ['data_spacial/' station '_low_6h.txt'];

HIDDEN_NUM =20;
ROUND_NUM = 4;
REPEAT_NUM = 10;

Train_Accuracy = 0;
Test_Accuracy = 0;
for k = 1:REPEAT_NUM
    d1 = load(f1);
    
    d1 = [ones(size(d1,1),1) d1(:,range)];
 
%    d1 = compRecord(d1);
    d0 = load(f0);
%    tmp_d0 = [max((d0(:,[15 21 27 33]))')' min((d0(:,[15 21 27 33]))')'];
    d0 = [zeros(size(d0,1),1) d0(:,range)];
%    d0 = compRecord(d0);
    d0 = d0(randperm(length(d0)),:); 
    d0 = d0(1:size(d1,1),:);
    d = [d0' d1']';
    
%    [~,tmp_id] = max((abs(d(:,2:6)))');
%    tmp_id = tmp_id'+1
%    new_d = []
%    for i = 1:size(d,1)
%        new_d = [new_d;d(i,1) d(i,tmp_id(i))];
%    end
%    d = new_d;
    tmp = [max((d(:,2:6))')' min((d(:,2:6))')'];
    d = [d(:,1) tmp];
    d = d(randperm(length(d)),:); 
    d = myNormalize(d);

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
        [Tr_acc, Te_acc] = my_ELM(Tr, Te, 1, HIDDEN_NUM, 'sig');
        Train_Accuracy = Train_Accuracy + Tr_acc;
        Test_Accuracy = Test_Accuracy + Te_acc;
    end
end
Train_Accuracy = Train_Accuracy/(ROUND_NUM*REPEAT_NUM);
Test_Accuracy = Test_Accuracy/(ROUND_NUM*REPEAT_NUM);
fprintf('Train_Accuracy: %f \n',Train_Accuracy);
fprintf('Test_Accuracy: %f \n',Test_Accuracy);

end

function [r_d] = compRecord(d)
    for col = 2:size(d,2)
        d = d(find(d(:,col)~=-1),:);
    end
    r_d = d;
end

function [n_d] = myNormalize(d)
    for col = 2:size(d,2)
        ma = max(d(:,col));
        mi = min(d(:,col));
        d(:,col) = (d(:,col)-mi)/(ma-mi);
    end
    n_d = d;
end

