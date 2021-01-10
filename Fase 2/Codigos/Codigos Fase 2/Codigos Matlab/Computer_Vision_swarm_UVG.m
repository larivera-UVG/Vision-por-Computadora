%% Jose Pablo Guerra 
% Codigo base para la herramienta de toma de pose de robotica swarm para la
% mesa de la UVG en version Matlab.
% Basado en el c�digo de Andr� Rodas para la Fase 1 de este proyecto. 

%% Version 0.0.1
% De momento se tiene la detecci�n de la c�mara y captura de foto
% Detecci�n de bordes y ubicaci�n de centros -falta ubicaci�n del �ngulo de
% rotaci�n.
% Creaci�n de la funci�n para generar marcadores visuales de
% identificaci�n.

%% Version 0.1.0
% Correcci�n al ploteo de las figuras y la posici�n del centro en la mesa
% f�sica Robotat.

%% Version 0.2.0
% Ajuste a la calibracion. Encuentra las 4 esquinas de intereses y corrige
% la perspectiva. Falta recortar la imagen en esas 4 esquinas para que la
% calibracion este completa. 

%% Para la detecci�n y captura de foto con la c�mara web
clear;
clf;
webcamlist
%Se requiere instalar un add on extra al momento de utilizar webcamlis

cam = webcam();
img = snapshot(cam);
figure(1);
imshow(img)

%% Para la calibracion
%clear;
%clf;
close all;  % Close all figures (except those of imtool.)
%anchoMesa = 16.0;
%largoMesa = 24.0;


%I = imread('Calibsnapshot.png');
I=img;
[rows, columns, numberOfColorChannels] = size(I);
GlobalHeigth = columns;
GlobalWidth = rows;

figure(3);
imshow(I);
I=rgb2gray(I);

BW1 = edge(I,'Canny',0.55);
B = bwboundaries(BW1,'noholes');

max_size = 1;
center_count = 1;

centers_esquinas = [];

for i=1:length(B)
    C = cell2mat(B(i));
    Cont = C';
    boundingBox = minBoundingBox(Cont);
    C2 = boundingBox(:,2);
    C4 = boundingBox(:,4);
    C3 = boundingBox(:,4);
    sizeX = abs(C2(1) - C4(1));
    sizeY = abs(C2(2) - C4(2));
    
    
    C1 = boundingBox(:,1);
    figure(52);
    plot(boundingBox(2,[1:end 1]),boundingBox(1,[1:end 1]),'r');
    hold on;
    axis equal
    if sizeX > max_size || sizeY > max_size
    
    Point2 = [(C2(1)+C4(1))/2,(C2(2)+C4(2))/2];
    
    Cx = Point2(1);
    Cy = Point2(2);
    X = abs(C1(1) - C2(1));
    Y = abs(C1(2) - C4(2));    
    
    dummy_center = [Point2(2),Point2(1)];
    
    
    centers_esquinas(center_count,:) = dummy_center; %[x,y] ese

    plot(Point2(2),Point2(1),'go');
    axis equal
    
    center_count=center_count+1;

    end

    %pause(2);
end

esquinas_temporales = zeros(4,2);
for index = 1:2
        k = find(centers_esquinas(:,2) == min(centers_esquinas(:,2)));
        esquinas_temporales(index,:) = centers_esquinas(k,:);
        centers_esquinas(k,:) = [];
end
for index = 3:4
        k = find(centers_esquinas(:,2) == max(centers_esquinas(:,2)));
        esquinas_temporales(index,:) = centers_esquinas(k,:);
        centers_esquinas(k,:) = [];
end


final_points=[esquinas_temporales(1,:);esquinas_temporales(3,:);esquinas_temporales(2,:);esquinas_temporales(4,:)];



initial_points=[0 0;size(I,1) 0;size(I,1) size(I,2);0 size(I,2)];

tform = fitgeotrans(final_points,initial_points,'NonreflectiveSimilarity');


out = imwarp(I,tform);

figure(60);
subplot(1,2,1)
imshow(out);
subplot(1,2,2)
imshow(I);


%% Para la detecci�n de bordes y ubicaci�n de los marcadores en la mesa
%clear;
pause(5);
%clf;
%close all;  % Close all figures (except those of imtool.)
anchoMesa = 16.0;
largoMesa = 24.0;


%I = imread('Calibsnapshot.png');
I=img;
[rows, columns, numberOfColorChannels] = size(I);
GlobalHeigth = columns;
GlobalWidth = rows;

figure(3);
imshow(I);
I=rgb2gray(I);

BW1 = edge(I,'Canny',0.7);
B = bwboundaries(BW1,'noholes');

max_size = 110;
center_count = 1;
centers = [];

for i=1:length(B)
    C = cell2mat(B(i));
    Cont = C';
    boundingBox = minBoundingBox(Cont);
    C2 = boundingBox(:,2);
    C4 = boundingBox(:,4);
    C3 = boundingBox(:,4);
    sizeX = abs(C2(1) - C4(1));
    sizeY = abs(C2(2) - C4(2));
    
    
    C1 = boundingBox(:,1);
    figure(42);
    plot(boundingBox(2,[1:end 1]),boundingBox(1,[1:end 1]),'r');
    hold on;
    axis equal
    if sizeX > max_size || sizeY > max_size
    
    Point2 = [(C2(1)+C4(1))/2,(C2(2)+C4(2))/2];
    
    Cx = Point2(1);
    Cy = Point2(2);
    X = abs(C1(1) - C2(1));
    Y = abs(C1(2) - C4(2));
    %angle = atand(X/Y)
    
    
    dummy_center = [Point2(1),Point2(2)];
    
    
    centers(center_count,:) = dummy_center;
    

    plot(Point2(2),Point2(1),'go');
    axis equal
    
%     I2 = imcrop(I,[C2(1)-X, C2(2)-Y, (Cx+X), (Cy+Y)]);
%     figure(105);
%     hold on;
%     imshow(I2);
%     
%     pause(5);
    
    center_count=center_count+1;

    end

    %pause(2);
end

positions = zeros(length(centers),2);
for i = 1:length(centers)
    tempFloatX = (anchoMesa/GlobalWidth) * centers(i,2);
    tempFloatY = (largoMesa/GlobalHeigth) * centers(i,1);
    %angles = atand(tempFloatY/tempFloatX);
    positions(i,:) = [tempFloatX tempFloatY];
end

%% Para probar la funcion de crear codigos, descomentar esta seccion o correr solamente esta
nombre = 'Codigo_ejemplo.png';
Cod = CreadorCodigos(40,nombre);
figure(2);
imshow(Cod);