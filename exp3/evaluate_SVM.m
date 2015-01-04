function evaluate_ELM( range,station )
%EVALUATE_ELM Summary of this function goes here
%   Detailed explanation goes here
%Local air
station = 'gucheng';
range = [2:7];

f1 = ['data/' station '_decrease.txt'];
f0 = ['data/' station '_high.txt'];

HIDDEN_NUM = 50;
ROUND_NUM = 4;
REPEAT_NUM = 10;

Train_Accuracy = 0;
Test_Accuracy = 0;
for k = 1:REPEAT_NUM
    d1 = load(f1);
%    tmp_d1 = [max((d1(:,[15 21 27 33]))')' min((d1(:,[15 21 27 33]))')'];
    d1 = [ones(size(d1,1),1) d1(:,range)];
%    d1 = compRecord(d1);
    d0 = load(f0);
%    tmp_d0 = [max((d0(:,[15 21 27 33]))')' min((d0(:,[15 21 27 33]))')'];
    d0 = [zeros(size(d0,1),1) d0(:,range)];
%    d0 = compRecord(d0);
    d0 = d0(randperm(length(d0)),:); 
    d0 = d0(1:size(d1,1),:);
    d = [d0' d1']';
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
        %[Tr_acc, Te_acc] = my_ELM(Tr, Te, 1, HIDDEN_NUM, 'sig');
        svmstruct = svmtrain(Tr(:,1),Tr(:,2:size(Tr,2)));
        [a,Te_acc,prob] = svmpredict(Te(:,1),Te(:,2:size(Te,2)),svmstruct);
        Test_Accuracy = Test_Accuracy + Te_acc;
    end
end
Test_Accuracy = Test_Accuracy/(ROUND_NUM*REPEAT_NUM);
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

