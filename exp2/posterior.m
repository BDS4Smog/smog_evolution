function posterior( input_args )
%POSTERIOR Summary of this function goes here
%   Detailed explanation goes here
station = 'gucheng';
col = 14;
left = 45;
right = 135;
f1 = ['data/' station '_decrease.txt'];
f0 = ['data/' station '_high.txt'];
d1 = load(f1);
d1 = d1(:,col);
d0 = load(f0);
d0 = d0(:,col);
d = [d0' d1']';
d = d(find(d(:,1)~=-1),:);
p_s = size(d1,1)/size(d,1)
p_x = size(find(d(:,1)>=left & d(:,1)<=right),1)/size(d,1)
p_x_s = size(find(d1(:,1)>=left & d1(:,1)<=right),1)/size(d1,1)
p_s_x = p_x_s*p_s/p_x;
fprintf('prior probability: %f, posterior probability: %f \n',p_s,p_s_x);
end

