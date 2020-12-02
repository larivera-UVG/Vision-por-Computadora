% %clear;
% %webcamlist
% %Se requiere instalar un add on extra al momento de utilizar webcamlis
% 
% %cam = webcam();
% img = snapshot(cam);
% figure(1);
% imshow(img)
% 
clear;
clf;
anchoMesa = 16.0;
largoMesa = 24.0;

I = imread('Calibsnapshot.png');
[rows, columns, numberOfColorChannels] = size(I);
GlobalHeigth = columns;
GlobalWidth = rows;

figure(3);
imshow(I);
I=rgb2gray(I);

BW1 = edge(I,'Canny',0.7);
figure(2);
B = bwboundaries(BW1);
imshow(BW1);

max_size = 110;
center_count = 1;
for i=1:length(B)
    C = cell2mat(B(i));
    Cont = C';
    boundingBox = minBoundingBox(Cont);
    C2 = boundingBox(:,2);
    C4 = boundingBox(:,4);
    sizeX = abs(C2(1) - C4(1))
    sizeY = abs(C2(2) - C4(2))
    
    figure(42);
    plot(boundingBox(1,[1:end 1]),boundingBox(2,[1:end 1]),'r')
    hold on;
    axis equal
    if sizeX > max_size || sizeY > max_size
    Point2 = [(C2(1)+C4(1))/2,(C2(2)+C4(2))/2];
    dummy_center = [Point2(1),Point2(2)];
    centers(center_count,:) = dummy_center;
    center_count=center_count+1;

    plot(Point2(1),Point2(2),'go');
    axis equal
    end
    %pause(2);
end

tempFloatX = (anchoMesa/GlobalWidth) * centers(length(centers),1);
tempFloatY = (largoMesa/GlobalHeigth) * centers(length(centers),2);

% 
% figure(42);
% %plot(boundingBox(1,[1:end 1]),boundingBox(2,[1:end 1]),'r')
% hold on;
% plot(Point2(1),Point2(2),'go');
% axis equal
% hold off;

%% Para probar la funcion de crear codigos, descomentar esta seccion o correr solamente esta
% nombre = 'Codigo_ejemplo.png';
% Cod = CreadorCodigos(35,nombre);
% figure(2);
% imshow(Cod);