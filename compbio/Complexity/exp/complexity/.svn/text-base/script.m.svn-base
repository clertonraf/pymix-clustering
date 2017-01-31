% analizys of correlation

data = importdata('res_all.csv')
text = data.textdata
data = data.data

% relevant complexity features
features = 8 + [10 12 14:16 19]
%features = [2 5 7 10 12 15]
data(:,features) = log(data(:,features));

%methods = [1 3 4 6 8 9 11 13 14 16]
methods = features

%
featuresPCA = 8 + [10 14:16 19]

% pca data
alldata = [data(:,featuresPCA)];
normdata =  (alldata - repmat(mean(alldata),size(alldata,1),1))./(repmat(std(alldata),size(alldata,1),1)+0.001)
covx = cov(normdata);
[COEFF,latent,explained] = pcacov(covx);
data(:,features(end)+1) = normdata*COEFF(:,1);
%features = [features features(end)+1];
%text{1,features(end)+1} = '1st PCA';

data(:,15) = log(data(:,15));


[v,i] = min(data(:,methods)');
text(1,methods(i)+1)

for j=1:length(data)
    best(j) = data(j,methods(i(j)))
end    

%data(:,features(end)+1) = best;
%methods = [methods features(end)+1];
%text{1,features(end)+2} = 'Best';

mappingMethods = [ 1 2 2 2 3 3 3 4 4 4];
mappingSelections = [ 1 2 3 4 2 3 4 2 3 4];

%figure
%gplotmatrix(best',data(:,features),mappingMethods(i))
%figure
%gplotmatrix(best',data(:,features),mappingSelections(i))


%data(:,1:7) = rank

[H,AX,BigAx,P,PAx]=plotmatrix(data(:,methods), data(:,features));
%[r,p] = corrcoef([data(:,methods) data(:,features)])

pos = max(data(:,features)) - (max(data(:,features)) - min(data(:,features)))*0.10
pos(2) = pos(2) - 0.5 
pos(6) = pos(6) + 0.4
pos(4) = pos(4) + 0.05
ypos = [0 300; 0 1.4; -0.03 0.43; 0.4 1.15; 0.0 0.4; 1.4 5.4; -4 5.7]
ctm = 0
for i=methods % methods
        ctm = ctm + 1
        indices = ~isnan(data(:,i));
        [r,p] = corrcoef([data(indices,i) data(indices,features)]);
        [x,y] = find(p(2:end,1)<0.01);
     
        text(1,i+1)
        text(1,features(x)+1)
        ct=1;
        r = r*100;
        r = round(r);
        r = r/100;
        ct = 1;
        for j=features
          ylabel(AX(ct,1),text(1,j+1));
          set(AX(ct,ctm),'FontSize',12);
          ylim(AX(ct,ctm),ypos(ct,:));
          if p(1,ct+1) > 0.01
            title(AX(ct,ctm),r(1,ct+1),'Position',[5,pos(ct)]);
          else              
            title(AX(ct,ctm),r(1,ct+1),'Position',[5,pos(ct)],'Color','r');            
          end
          ct = ct + 1;
        end   
        xlabel(AX(7,ctm),text(1,i+1));         
end


%%for i=1:length():
%set(AX(ct,ctm),'FontSize',12);

%plot3(data(:,1),data(:,21),data(:,22),'.g')
%hold on 
%plot3(data(:,2),data(:,21),data(:,22),'.r')
%plot3(data(:,4),data(:,21),data(:,22),'.b')
%plot3(data(:,6),data(:,21),data(:,22),'.c')
%plot3(data(:,8),data(:,21),data(:,22),'.y')


