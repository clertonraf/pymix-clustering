cons(1,2,:,:) = dlmread('cons-res-lab-fil-172-4.txt');
cons(2,2,:,:) = dlmread('cons-res-cons-fil-2-172-4.txt');
cons(2,3,:,:) = dlmread('cons-res-cons-fil-1723-4.txt');



for j=1:2    
  [ordcons,clustid,ordindex,coph] = nmforderconsensus(reshape(cons(j,:,:,:),5,52,52),2,3); 
  figure
  for i=1:5
    figure
    pos = (1:52)+0.5;
    %size(ordcons(j,i,:,:),52,52)
    i,j
    pcolor(reshape(ordcons(i,:,:),52,52))
    set(gca,'YTick',pos)
    set(gca,'YTickLabel',ordindex(:,i));
    set(gca,'XTick',pos)
    set(gca,'XTickLabel',ordindex(:,i));
    set(gca,'YDir','reverse')
  end
end
