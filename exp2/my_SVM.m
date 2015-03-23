function [TrainingAccuracy, TestingAccuracy, precision, recall, f1_score,FPR,TPR,auc] = my_SVM(train_data, test_data)

train_feature = [train_data(:,2:end)];
train_raw_target = train_data(:,1);
svmstruct = svmtrain(train_raw_target,train_feature);


test_feature = [test_data(:,2:end)];
test_raw_target = test_data(:,1);

[a,Te_acc,prob] = svmpredict(test_raw_target,test_feature,svmstruct);

tmp = length(test_data(:,1));
T_Expected_2 = zeros(tmp,2);
for i=1:tmp
	T_Expected_2(i,test_data(i,1)+1)=1;
end
T_Exp_roc = test_raw_target;
T_Act_roc = -prob;

[FPR,TPR,T,auc] = perfcurve(T_Exp_roc',T_Act_roc',1);


label_Actual_whole = a;
label_Expected_whole = test_raw_target;
%[~,label_Actual_whole] = max(T_Actual,[],2)
TestingAccuracy = length(find(label_Expected_whole==label_Actual_whole))/length(label_Actual_whole)
positives_Actural = length(find(label_Actual_whole==1))
positives_Expected = length(find(label_Expected_whole==1))
positives_correct = length(find(label_Expected_whole==label_Actual_whole & label_Actual_whole==1))
precision = positives_correct/positives_Actural
recall = positives_correct/positives_Expected
f1_score = 2*precision*recall/(precision+recall)

sprintf('TestingAccuracy  = 0 is %f', TestingAccuracy);
TrainingAccuracy = 0;

end