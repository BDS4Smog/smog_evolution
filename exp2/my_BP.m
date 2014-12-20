function [TrainingAccuracy, TestingAccuracy, precision, recall, f1_score] = my_BP(train_data, test_data)

train_feature = [train_data(:,2:end)]';
train_raw_target = train_data(:,1);
tmp = length(train_raw_target);
train_target = zeros(tmp,2);
for i=1:tmp
	train_target(i,train_raw_target(i)+1)=1;
end

net = newff(minmax(train_feature),[10 2],{'logsig' 'purelin'},'trainlm');

net.trainparam.show = 50;
net.trainparam.epochs = 500;
net.trainparam.goal = 0.01 ;
net.trainParam.lr = 0.01 ;

net = train( net, train_feature , train_target' ) ;

test_feature = [test_data(:,2:end)]';
test_raw_target = test_data(:,1);

Y = sim(net, test_feature);

test_raw_target = test_raw_target+1
correct_count = 0;
[s1 s2] = size(Y);
for i=1:s2
	[~,Index] = max(Y(:,i));
	if(Index == test_raw_target(i))
		correct_count = correct_count+1;
	end
end
TestingAccuracy = correct_count/s2;

T_Actual = Y';
label_Expected_whole = test_raw_target;
[~,label_Actual_whole] = max(T_Actual,[],2)
positives_Actural = length(find(label_Actual_whole==2))
positives_Expected = length(find(label_Expected_whole==2))
positives_correct = length(find(label_Expected_whole==label_Actual_whole & label_Actual_whole==2))
precision = positives_correct/positives_Actural
recall = positives_correct/positives_Expected
f1_score = 2*precision*recall/(precision+recall)

sprintf('TestingAccuracy  = 0 is %f', TestingAccuracy);
TrainingAccuracy = 0;

end