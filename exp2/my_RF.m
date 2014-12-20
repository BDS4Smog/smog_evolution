function  [Tr_acc, Te_acc, tmp_precision, tmp_recall, tmp_f1_score] = my_RF(Tr, Te, nTrees)

train_features = Tr(:,2:end);
train_target = Tr(:,1);
test_features = Te(:,2:end);
label_Actual_whole = Te(:,1);

B = TreeBagger(nTrees,train_features,train_target,'Method','classification');
Y = B.predict(test_features)

tmp = cell2mat(Y)
label_Expected_whole = ones(length(Y),1);
for i=1:length(Y)
    if tmp(i)=='1'
        label_Expected_whole(i)=1;
    else
        label_Expected_whole(i)=0;
    end
end

Tr_acc =  0
Te_acc = length(find(label_Expected_whole==label_Actual_whole))
positives_Actural = length(find(label_Actual_whole==1))
positives_Expected = length(find(label_Expected_whole==1))
positives_correct = length(find(label_Expected_whole==label_Actual_whole & label_Actual_whole==1))
tmp_precision = positives_correct/positives_Actural
tmp_recall = positives_correct/positives_Expected
tmp_f1_score = 2*tmp_precision*tmp_recall/(tmp_precision+tmp_recall)

end