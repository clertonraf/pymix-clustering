function [d,n,noclasses,mf1,mf2,mn1,mn2,mn3,l1,l2,l1n,l2n] = data_complexity(filename)
% implementation of data complexity indices described in
% Complexity Measures of Supervised Classification Problems
% IEEE Transactions on Pattern Analysis and Machine Intelligence archive
%Volume 24 ,  Issue 3  (March 2002) table of contents
%Pages: 289 - 300  
% Year of Publication: 2002
%T. K. Ho 	
%M. Basu
%
% This codes requires the optmization toolbox and the Bayesian Network
% Toolbox (BNT)

filename
data = importdata(['data/' filename],'\t',2);
classes_labels = data.textdata(2,:);

% extract numerical representation of classes
[classes,noclasses] = extractClasses(classes_labels);

ct = 1
% calculate indices for all pairs of classes
for i=1:noclasses
  for j=(i+1):noclasses
      filter = (classes==i) | (classes==j);

      datanew = data.data(:,filter); % removing id collumns
      new_class = classes(filter);
      new_class(new_class==i) = 0;
      new_class(new_class==j) = 1;
      f1(ct) = fisherratio(datanew,new_class);
      f2(ct) = volumeOfOverlap(datanew,new_class);
      n1(ct) = mixtureIdentifiability(datanew,new_class);
      n2(ct) = ratioInterIntraNN(datanew,new_class);
      n3(ct) = nearestNeighbor(datanew,new_class);
      [l1aux,l2aux] =linearClass(datanew,new_class,0);
      [l1aux1,l2aux1] =linearClass(datanew,new_class,0.20);
      l1(ct) = l1aux;
      l2(ct) = l2aux;
      
      l1n(ct) = l1aux1;
      l2n(ct) = l2aux1;     
      
      ct = ct + 1;
  end
end

mf1 = mean(f1);
mf2 = mean(f2);
mn1 = mean(n1);
mn2 = mean(n2);
mn3 = mean(n3);
l1 = mean(l1);
l2= mean(l2);
l1n = mean(l1n);
l2n= mean(l2n);
d = size(data.data,2); % dimension
n = size(data.data,1); % elements



% indices for arbitrary number of classes 
end


  function fisher = fisherratio(data,classes_labels)
    % implementation of the fisher discriminant ratio (F1)
    data0 = data(:,classes_labels==0)';
    data1 = data(:,classes_labels==1)';
    
    fisherAll = power(mean(data0) - mean(data1),2)/(var(data0) + var(data1));
    fisher = max(fisherAll);
    
  end


  function volumeOverlap = volumeOfOverlap(data,classes_labels)
    % implementation of the volume of overllap region (F2)
    % i made it exponential, as it goes quickly to zero given dimension size
    data0 = data(:,classes_labels==0)';
    data1 = data(:,classes_labels==1)';
     
    % for all feature do
    volumeOverlap = 1;
    for i=1:size(data1,2)
        if ~isnan((nanmin(nanmax(data0(:,i)),nanmax(data1(:,i))) - nanmax(nanmin(data0(:,i)),nanmin(data1(:,i))))/(nanmax(nanmax(data0(:,i)),nanmax(data1(:,i))) - nanmin(nanmin(data0(:,i)),nanmin(data1(:,i)))))
          volumeOverlap = volumeOverlap*(nanmin(nanmax(data0(:,i)),nanmax(data1(:,i))) - nanmax(nanmin(data0(:,i)),nanmin(data1(:,i))))/(nanmax(nanmax(data0(:,i)),nanmax(data1(:,i))) - nanmin(nanmin(data0(:,i)),nanmin(data1(:,i))));
        end
    end
    
  end
  
  function interintra = ratioInterIntraNN(data,classes_labels)
     % ratio of inter/intra 1 nearest neigbohr (N2)
    % calculate euclidian distance
    dist = squareform(pdist(data'));       
    
    for i=1:size(dist,1)
        dist(i,i) = 10000000000000.00; % make diagonal value to be high
        intra(i) = min(dist(i,classes_labels==classes_labels(i))); % minimun distance of same class
        inter(i) = min(dist(i,classes_labels~=classes_labels(i))); % minimun distance of distinct class
    end
    interintra = mean(intra)/mean(inter) ;
  end

  function identifiability = mixtureIdentifiability(data,classes_labels)
    % implementation of the volume of overllap region (N1)
    
    % define what distance to use !!!
    dist = squareform(pdist(data'));     
    % compute minimum spannig tree
    G = minimum_spanning_tree(dist);
    T = mk_rooted_tree(G, 1);
    T=full(T);
    
    % check how many interclass connections there are
    ct = 0;
    for i=1:size(T,1)
      for j=1:size(T,1)
        if T(i,j) == 1 & classes_labels(i) ~= classes_labels(j) % check connected examples with wrong classes
          ct = ct + 1;
        end
      end
    end
           
    volumeOverlap = 0;
    % normalize by the number of edges
    identifiability = ct/(size(T,1)-1) ;
  end
  
  function nearest = nearestNeighbor(data,classes_labels)
    % error rate of 1 NN (N3)
    
    % define what distance to use !!!
    dist = squareform(pdist(data'));     

    % check for nearest neighborhs erros
    ct = 0;
    for i=1:size(dist,1)
        dist(i,i) = 10000000000000.00; % make diagonal value to be high
        [v,j]= min(dist(i,:));
        if classes_labels(i) ~= classes_labels(j)
            ct = ct + 1;
        end
    end           
    nearest = ct/size(dist,1);
  end
  
  function [fval,error] = linearClass(data,classes_labels,rand)
    % calculates the classifier (l2) and sum or error vector (t) (l1)
    % of a linear programing based classifier
    
    if rand > 0
        indices = (random('uniform',0,1,1,length(classes_labels)) < rand);
        for i=1:length(indices)
            if indices(i) == 1
                if classes_labels(i) == 1
                    classes_labels(i) = 0
                else
                    classes_labels(i) = 1
                end
            end
        end

        sum(indices)
    end
    
    data0 = -data(:,classes_labels==0)';
    data1 = data(:,classes_labels==1)';
    data = [data0;data1];
    
    d = size(data,2); % dimension
    e = size(data,1); % elements
    
    % linear programing problem
    % opmize f*x
    % given A*x =< b
    % for linear classification the problem is
    % optmize t*1
    % given D*w + 1 >= 1
    %             t >= 0
    % where D is the data
    %       w are the plane coeficients
    %       t are the sample error
    % this problem can be coded as the linear form as
    % x = [w t]
    % f = [0^d 1^n] 
    % A = [-D -I^(n,n); O^(d,n) I^(n,n)] 
    % b = [1^n 0^n]
    %where I^(n,n) is a n by n identity matrix
    
    f = [zeros(d,1)' ones(e,1)'];
    A = [-data -eye(e); -zeros(size(data)) -eye(e)];
    b = [-ones(e,1) zeros(e,1)];
    [x,fval,exitflag,output,lambda] = linprog(f,A,b);    
    
    % calculating t*1 and normalizing by number of example
    fval = fval/e;
    error = sum(x((d+1):end))/e;

    w = x(1:d); % weigths 
    data = [-data0;data1]; % data without sign
    class = data*w; % classifier
    classes_labels = [-ones([size(data0,1) 1])',ones([size(data1,1) 1])']
    error = 1- sum(sign(class)' == classes_labels)/e; % counting classfication error
  end


  function [classes,noclasses] = extractClasses(classes_labels)

      ct = 1;
      current = classes_labels{2};
      labels{1} = current;
      for i=2:length(classes_labels)
        assigned = 0;
        for j=1:length(labels)            
          if strcmp(labels{j},classes_labels{i})oldsvn
            classes(i-1) = j;
            assigned = 1;
          end
        end
        if ~assigned
          labels{j+1}=classes_labels{i};
          classes(i-1) = j+1;
        end
      end  
      noclasses = max(classes);
  end
  



    