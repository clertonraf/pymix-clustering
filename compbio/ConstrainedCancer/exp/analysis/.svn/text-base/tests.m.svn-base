%data(:,1) = importdata('res-all-res-cons-fil-4-35-4-4.txt'); % Const 4 
%data(:,2) = importdata('res-all-res-lab-fil-17-2-4.txt'); % Class
%data(:,3) = importdata('res-all-res-cons-fil-2-17-2-4.txt'); % Const 2
%data(:,4) = importdata('res-all-res-cons-fil-3-17-3-4.txt'); % Const 3
%data(:,5) = importdata('res-all-res-cons-fil-2-17-all-2-4.txt'); % Const all 2
%data(:,6) = importdata('res-all-res-cons-fil-3-17-all-3-4.txt'); % Const all 3

files = {'alizadeh-2000-v1.txt',   
         'alizadeh-2000-v2.txt',
         %'alizadeh-2000-v3.txt',   
         'armstrong-2002-v1.txt',
         'armstrong-2002-v2.txt',
         %'bittner-2000.txt',   
         'chen-2002.txt',
         'golub-1999-v1.txt',
         'golub-1999-v2.txt',
         %'nutt-2003-v1.txt', 
    	 'nutt-2003-v2.txt',
         'nutt-2003-v3.txt',
         %'pomeroy-2002-v1.txt'
         %'pomeroy-2002-v2.txt',
         %'shipp-2002-v1.txt',
	     'singh-2002.txt',
         'yeoh-2002-v1.txt',
         'yeoh-2002-v2.txt'}
   

for i=1:size(files)

  data = [];

  data = importdata(files{i})
  [p,table,stats] = friedman(data(:,1:3),1,'off')
  [c,m,h,nms] = multcompare(stats,'estimate','friedman','ctype','lsd')

    for k=1:1
      for j=(k+1):size(data,2)
      [h(i,j), pvalue(i,j), ci, stats] = ttest(data(:,k)',data(:,j)',0.05);
    end
  end



  means(i,1:size(data,2)) = mean(data)
  stds(i,1:size(data,2)) = std(data)
  pause

end


%for i=1:6
%  for j=(i+1):6
%    [h(i,j), pvalue(i,j), ci, stats] = ttest(data(:,i)',data(:,j)',0.05,'right');
%  end
%end


%for i=1:6
%  for j=1:3
%    [hi(i,j), pvaluei(i,j), ci, stats] = ttest(data(:,i)',dataind(j),0.05,'left');
%  end
%end

%pvalue

%pvaluei
