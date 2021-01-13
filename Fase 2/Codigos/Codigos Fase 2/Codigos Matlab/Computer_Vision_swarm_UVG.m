%% Jose Pablo Guerra 
% Codigo base para la herramienta de toma de pose de robotica swarm para la
% mesa de la UVG en version Matlab.
% Basado en el código de André Rodas para la Fase 1 de este proyecto. 

%% Version 0.0.1
% De momento se tiene la detección de la cámara y captura de foto
% Detección de bordes y ubicación de centros -falta ubicación del ángulo de
% rotación.
% Creación de la función para generar marcadores visuales de
% identificación.

%% Version 0.1.0
% Corrección al ploteo de las figuras y la posición del centro en la mesa
% física Robotat.

%% Version 0.2.0
% Ajuste a la calibracion. Encuentra las 4 esquinas de intereses y corrige
% la perspectiva. Falta recortar la imagen en esas 4 esquinas para que la
% calibracion este completa. 

%Para esta version (una version cercana a la final) queda pendiente:
% -Recortar la imagen con correccion de perspectiva para ubicar el area de
% interes en esos 4 puntos.
% -Ubicar los contornos de los marcadores y proceder a extraer el ID de
% cada uno.
% -Encontrar el angulo de rotacion de cada marcador identificado. 

%% Para la detección y captura de foto con la cámara web
clear; %para limpiar variables, evita un error con la variable webcam()
clf; %limpia figuras

webcamlist %Se requiere instalar un add on extra al momento de utilizar webcamlist, lista las camaras encontradas

cam = webcam(); %Crea el objeto camara para optar a sus opciones
img = snapshot(cam); %captura fotografia

%muestra la imagen capturada
figure(1);
imshow(img)

%% Para la calibracion
%clear;
%clf;
%close all;  % Close all figures (except those of imtool.)
%anchoMesa = 16.0;
%largoMesa = 24.0;


%I = imread('Calibsnapshot.png');
I=img; %agrega la imagen capturada a una variable para usarla. 

%[rows, columns, numberOfColorChannels] = size(I);
%GlobalHeigth = columns;
%GlobalWidth = rows;

%muestra la imagen 
figure(3);
imshow(I);

%para utilizar Canny, explicitimante hay que convertir la fotografia a
%blanco y negro con la funcion rgb2gray()
I=rgb2gray(I);


BW1 = edge(I,'Canny',0.55); %edge es la funcion de Canny detector para Matlab
B = bwboundaries(BW1,'noholes'); %bwboundaries() funcion que detecta los contornos en matlab.

[centers_esquinas, esquinas_temporales] = center_detection(52,B,1, 'FindCorners'); %funcion para detectar esquinas y contornos de interes.

% max_size = 1;
% center_count = 1;

%centers_esquinas = [];

% for i=1:length(B)
%     C = cell2mat(B(i));
%     Cont = C';
%     boundingBox = minBoundingBox(Cont);
%     C2 = boundingBox(:,2);
%     C4 = boundingBox(:,4);
%     C3 = boundingBox(:,4);
%     sizeX = abs(C2(1) - C4(1));
%     sizeY = abs(C2(2) - C4(2));
%     
%     
%     C1 = boundingBox(:,1);
%     figure(52);
%     plot(boundingBox(2,[1:end 1]),boundingBox(1,[1:end 1]),'r');
%     hold on;
%     axis equal
%     if sizeX > max_size || sizeY > max_size
%     
%     Point2 = [(C2(1)+C4(1))/2,(C2(2)+C4(2))/2];
%     
%     Cx = Point2(1);
%     Cy = Point2(2);
%     X = abs(C1(1) - C2(1));
%     Y = abs(C1(2) - C4(2));    
%     
%     dummy_center = [Point2(2),Point2(1)];
%     
%     
%     centers_esquinas(center_count,:) = dummy_center; %[x,y] ese
% 
%     plot(Point2(2),Point2(1),'go');
%     axis equal
%     
%     center_count=center_count+1;
% 
%     end
% 
%     %pause(2);
% end

% esquinas_temporales = zeros(4,2);
% for index = 1:2
%         k = find(centers_esquinas(:,2) == min(centers_esquinas(:,2)));
%         esquinas_temporales(index,:) = centers_esquinas(k,:);
%         centers_esquinas(k,:) = [];
% end
% for index = 3:4
%         k = find(centers_esquinas(:,2) == max(centers_esquinas(:,2)));
%         esquinas_temporales(index,:) = centers_esquinas(k,:);
%         centers_esquinas(k,:) = [];
% end


final_points=[esquinas_temporales(1,:);esquinas_temporales(3,:);...
    esquinas_temporales(2,:);esquinas_temporales(4,:)]; %reordnea las esquinas para la correcion de perspectiva



initial_points=[0 0;size(I,1) 0;size(I,1) size(I,2);0 size(I,2)]; %puntos iniciales en la imagen original
%es decir, el tamaño maximo de la imagen original

%fitgeotrans(puntos_moviles, puntos_fijos, tipo). 
%Esta funcion realiza la transformacion de perspectiva. Los puntos moviles 
%son los puntos (en la imagen original) hacia los que se desea hacer la 
%conversion, en este caso, las esquinas encontradas con la funcion anterior. 
%Los puntos fijos son los puntos de la imagen original para hacer la
%transformación. Retorna un objeto tform, matriz de transformada.
tform = fitgeotrans(final_points,initial_points,'NonreflectiveSimilarity');


out = imwarp(I,tform); %aplica la transformación

%muestra el resultado. 
figure(60);
subplot(1,2,1)
imshow(out);
subplot(1,2,2)
imshow(I);


%% Para la detección de bordes y ubicación de los marcadores en la mesa
%clear;
pause(5); %pausa para ver imagenes anteriores

%dimensiones fisicas de la mesa, es necesario para encontrar correctamente
%la posicion fisica.
anchoMesa = 16.0;
largoMesa = 24.0;


I = imread('Calibsnapshot.png');
%I=img;

[rows, columns, numberOfColorChannels] = size(I); %obtiene el tamaño y el ancho de la imagen
GlobalHeigth = columns;
GlobalWidth = rows;

%muestra la imagen a identificar.
figure(3);
imshow(I);

%Convierte a escala de grises para la detección de los bordes
I=rgb2gray(I);

BW1 = edge(I,'Canny',0.7); %bordes de Canny
B = bwboundaries(BW1,'noholes'); %detección de contornos

max_size = 110; %para ubicar solamente marcadores y no cosas mas pequeñas
%center_count = 1;

centers = center_detection(82,B,max_size, 'NoFindCorners'); %funcion para detectar esquinas y contornos de interes.

% for i=1:length(B)
%     C = cell2mat(B(i));
%     Cont = C';
%     boundingBox = minBoundingBox(Cont);
%     C2 = boundingBox(:,2);
%     C4 = boundingBox(:,4);
%     C3 = boundingBox(:,4);
%     sizeX = abs(C2(1) - C4(1));
%     sizeY = abs(C2(2) - C4(2));
%     
%     
%     C1 = boundingBox(:,1);
%     figure(42);
%     plot(boundingBox(2,[1:end 1]),boundingBox(1,[1:end 1]),'r');
%     hold on;
%     axis equal
%     if sizeX > max_size || sizeY > max_size
%     
%     Point2 = [(C2(1)+C4(1))/2,(C2(2)+C4(2))/2];
%     
%     Cx = Point2(1);
%     Cy = Point2(2);
%     X = abs(C1(1) - C2(1));
%     Y = abs(C1(2) - C4(2));
%     %angle = atand(X/Y)
%     
%     
%     dummy_center = [Point2(1),Point2(2)];
%     
%     
%     centers(center_count,:) = dummy_center;
%     
% 
%     plot(Point2(2),Point2(1),'go');
%     axis equal
%     
% %     I2 = imcrop(I,[C2(1)-X, C2(2)-Y, (Cx+X), (Cy+Y)]);
% %     figure(105);
% %     hold on;
% %     imshow(I2);
% %     
% %     pause(5);
%     
%     center_count=center_count+1;
% 
%     end
% 
%     %pause(2);
% end

%transforma los datos en pixeles hacia los datos fisicos mediante la
%conversion que se detalla:
% X = (anchomesa/Width) * Cx
% Y = (largomesa/Height) * Cy
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