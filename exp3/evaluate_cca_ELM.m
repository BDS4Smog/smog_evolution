function evaluate_cca_ELM( station )
%EVALUATE_CCA_ELM Summary of this function goes here

station = 'beijing';
version = '1';
type1 = 'decrease';
type2 = 'high';

KERNEL = 0;

HIDDEN_NUM = 100;
ROUND_NUM = 4;
REPEAT_NUM = 50;
LIMIT_OF_EMPTY = 6;
   
view_d1 = loadView(1, station, version, type1, type2);
view_d2 = loadView(2, station, version, type1, type2);
[view_d1,view_d2] = extract_record(view_d1,view_d2,LIMIT_OF_EMPTY);
[view_d1,view_d2] = equalize_label(view_d1,view_d2);

if KERNEL ==0
    [view_d1,view_d2] = myCCA(view_d1,view_d2);
else
    [view_d1,view_d2] = myKCCA(view_d1,view_d2);
   
end

d = [view_d1 view_d2(:,2:size(view_d2,2))];
d = d(randperm(length(d)),:); 
d = myNormalize(d);
    
Train_Accuracy = 0;
Test_Accuracy = 0; 
precision = 0;
recall = 0;
f1_score = 0;
for k = 1:REPEAT_NUM    
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
        [Tr_acc, Te_acc, tmp_precision, tmp_recall, tmp_f1_score] = my_ELM(Tr, Te, 1, HIDDEN_NUM, 'sig');
        Train_Accuracy = Train_Accuracy + Tr_acc;
        Test_Accuracy = Test_Accuracy + Te_acc;
        precision = precision+tmp_precision
        recall = recall+tmp_recall
        f1_score = f1_score+tmp_f1_score
    end
end

Train_Accuracy = Train_Accuracy/(ROUND_NUM*REPEAT_NUM);
Test_Accuracy = Test_Accuracy/(ROUND_NUM*REPEAT_NUM);
precision = precision/(REPEAT_NUM*ROUND_NUM);
recall = recall/(REPEAT_NUM*ROUND_NUM);
f1_score = f1_score/(REPEAT_NUM*ROUND_NUM);
fprintf('Train_Accuracy: %f \n',Train_Accuracy);
fprintf('Test_Accuracy: %f \n',Test_Accuracy);
fprintf('Test_precision: %f \n',precision);
fprintf('Test_recall: %f \n',recall);
fprintf('Test_f1_score: %f \n',f1_score);
fprintf('Number of records: %d \n',size(d,1));

end


function [view_d] = loadView(view_num, station, version, type1, type2)
    
    air_range = 2:7;
    mete_range = 2:8;
    air_surround_range = 2:6;
    mete_surround_range = 2:36;
    air_surround_diff_range = 2:6;
    traffic_range = 2:9;
    checkin_range = 2:12;
    om_range = 2:9;

    air_f1 = ['air/' station '_' type1 version '.txt'];
    air_f0 = ['air/' station '_' type2 version '.txt'];
    mete_f1 = ['mete/' station '_' type1 version '.txt'];
    mete_f0 = ['mete/' station '_' type2 version '.txt'];
    air_surround_f1 = ['air_surround/' station '_' type1 version '.txt'];
    air_surround_f0 = ['air_surround/' station '_' type2 version '.txt'];
    mete_surround_f1 = ['mete_surround/' station '_' type1 version '.txt'];
    mete_surround_f0 = ['mete_surround/' station '_' type2 version '.txt'];
    air_surround_diff_f1 = ['air_surround_diff/' station '_' type1 version '.txt'];
    air_surround_diff_f0 = ['air_surround_diff/' station '_' type2 version '.txt'];
    traffic_f1 = ['traffic_new/' station '_' type1 version '.txt'];
    traffic_f0 = ['traffic_new/' station '_' type2 version '.txt'];
    checkin_f1 = ['check-in/' station '_' type1 version '.txt'];
    checkin_f0 = ['check-in/' station '_' type2 version '.txt'];
    om_f1 = ['opinion_mining/' station '_' type1 version '.txt'];
    om_f0 = ['opinion_mining/' station '_' type2 version '.txt'];

    if view_num==1
        tmp_d = load(air_f1);
        d1 = tmp_d(:,air_range);
        tmp_d = load(air_f0);
        d0 = tmp_d(:,air_range);
    end
    if view_num==2
        tmp_d = load(mete_f1);
        d1 = tmp_d(:,mete_range);
        tmp_d = load(mete_f0);
        d0 = tmp_d(:,mete_range);
    end
    if view_num==3
        tmp_d = load(air_surround_f1);
        d1 = tmp_d(:,air_surround_range);
        tmp_d = load(air_surround_f0);
        d0 = tmp_d(:,air_surround_range);
    end
    if view_num==4
        tmp_d = load(mete_surround_f1);
        d1 = tmp_d(:,mete_surround_range);
        tmp_d = load(mete_surround_f0);
        d0 = tmp_d(:,mete_surround_range);
    end
    if view_num==5
        tmp_d = load(air_surround_diff_f1);
        d1 = tmp_d(:,air_surround_diff_range);
        tmp_d = load(air_surround_diff_f0);
        d0 = tmp_d(:,air_surround_diff_range);
    end
    if view_num==6
        tmp_d = load(traffic_f1);
        d1 = tmp_d(:,traffic_range);
        tmp_d = load(traffic_f0);
        d0 = tmp_d(:,traffic_range);
    end
    if view_num==7
        tmp_d = load(checkin_f1);
        d1 = tmp_d(:,checkin_range);
        tmp_d = load(checkin_f0);
        d0 = tmp_d(:,checkin_range);
    end
    if view_num==8
        tmp_d = load(om_f1);
        d1 = tmp_d(:,om_range);
        tmp_d = load(om_f0);
        d0 = tmp_d(:,om_range);
    end

    
    d1 = [ones(size(d1,1),1) d1];
    d0 = [zeros(size(d0,1),1) d0];
    view_d = [d1;d0];
    
end


function [d1,d2] = extract_record(view_d1, view_d2, limit)
    M=size(view_d1,1);
    indexes = [];
    for row = 1:M
        miss1 = size(find(view_d1(row,:)==-1),2);
        miss2 = size(find(view_d2(row,:)==-1),2);
        if((miss1+miss2)<=limit)
            indexes = [indexes row];
        end
    end
    d1 = view_d1(indexes,:);
    d2 = view_d2(indexes,:);
end

function [d1,d2] = equalize_label(view_d1,view_d2)
    indexes1 = find(view_d1(:,1)==1);
    num1 = length(indexes1);
    indexes0 = find(view_d1(:,1)==0);
    indexes0 = indexes0(randperm(length(indexes0)));
    indexes0 = indexes0(1:num1);
    d1 = view_d1([indexes1;indexes0],:);
    d2 = view_d2([indexes1;indexes0],:);
end

function [n_d] = myNormalize(d)
    for col = 2:size(d,2)
        ma = max(d(:,col));
        mi = min(d(:,col));
        d(:,col) = (d(:,col)-mi)/(ma-mi);
    end
    n_d = d;
end

function [d1,d2] = myCCA(view_d1,view_d2)
    [A B r U V] = canoncorr(view_d1(:,2:size(view_d1,2)),view_d2(:,2:size(view_d2,2)));
    d1 = [view_d1(:,1) U(:,1:size(U,2))];
    d2 = [view_d2(:,1) V(:,1:size(V,2))];
end

function [d1,d2] = myKCCA(view_d1,view_d2)
    kernel1 = {'gauss',1};
    kernel2 = {'gauss',1}; 
    reg = 1E-5;
    Mmax = 50;
    [y1,y2,beta] = km_kcca(view_d1(:,2:size(view_d1,2)),view_d2(:,2:size(view_d2,2)),kernel1,kernel2,reg,'ICD',Mmax);
    fprintf('Canonical correlation: %f\n',beta)
    d1 = [view_d1(:,1) y1];
    d2 = [view_d2(:,1) y2];
end

