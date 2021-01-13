#include "tomaposerobots.h"

#define SQRTDE2 1.41421356
#define MyPI 3.14159265

const float largoMesa = 16.0; //16 para el papel milimetrado
const float anchoMesa = 24.0; //24 para el papel milimetrado

int GlobalCodePixThreshold = 70;
int GlobalColorDifThreshold = 20;
int GlobalWidth, GlobalHeigth = 0;
Mat GlobalLambda, GlobalCroppedActualSnap;



/// NO SE USA
void updateRobotCodes(VectorRobots &_lastVRobotCodes, Mat _CropPhoto, int _CannyVinf, int _CannyVsup) {

    VectorRobots updatedRobots = getRobotCodes(_CropPhoto, _CannyVinf, _CannyVsup);
    for (int i = 0; i < _lastVRobotCodes.Vrobots.size(); i++)
    {
        int CurrentID = _lastVRobotCodes.Vrobots.at(i).id;
        int NewID = updatedRobots.buscarPosID_robot(CurrentID);
        vector<int> NewPose = updatedRobots.Vrobots.at(NewID).get_Pose();
        _lastVRobotCodes.Vrobots.at(i).set_Pose(NewPose.at(0), NewPose.at(1), NewPose.at(2));
    }

}
/// NO SE USA

///funcion
/// En multi-hilos debe ira esta funcion
VectorRobots getRobotCodes(Mat _CropPhoto, int _CannyVinf, int _CannyVsup)
{
    VectorRobots ActualRobots;
    Mat _CropGrayPhoto, _CannyPhoto;
    vector<vector<Point>> contornos;
    vector<Vec4i> jerarquia;

    GlobalCroppedActualSnap = _CropPhoto;
    //imshow("GlobalCroppedActualSnap", GlobalCroppedActualSnap);
    //waitKey(0);

    //float PixCodeSize = _CmCodeSize * (_CropPhoto.size().width / anchoMesa);
    //cout << "voy a hacer el procesamiento" << endl;
    cvtColor(_CropPhoto, _CropGrayPhoto, CV_BGR2GRAY);
    blur(_CropGrayPhoto, _CropGrayPhoto, Size(3, 3));
    Canny(_CropGrayPhoto, _CannyPhoto, _CannyVinf, _CannyVsup, 3);
    //imshow("canny", _CannyPhoto);
    //waitKey(0);
    findContours(_CannyPhoto, contornos, jerarquia, CV_RETR_EXTERNAL, CV_CHAIN_APPROX_SIMPLE, Point(0, 0));
    blur(_CropGrayPhoto, _CropGrayPhoto, Size(3, 3));
    //cout << "He finalizado todo el proceso de procesamiento" << endl;
    RotatedRect SingleRecCod, LastRecCod;
    for (int i = 0; i < contornos.size(); i++)
    {
        SingleRecCod = minAreaRect(contornos[i]);
        //cout << SingleRecCod.size.width << endl;
        //cout << SingleRecCod.size.height << endl;


        if ((SingleRecCod.size.width  > GlobalCodePixThreshold) && (SingleRecCod.size.height  > GlobalCodePixThreshold))
        {
            if (i == 0)
            {
                cout << "primer if, i = 0" << endl;
                ActualRobots.agregar_robot(getRobotfromSnapShot(SingleRecCod));
                LastRecCod = SingleRecCod;
            }
            else //if (((abs(SingleRecCod.center.x - LastRecCod.center.x) > GlobalCodePixThreshold) || (abs(SingleRecCod.center.y - LastRecCod.center.y) > GlobalCodePixThreshold)))
            {
                ActualRobots.agregar_robot(getRobotfromSnapShot(SingleRecCod));
                LastRecCod = SingleRecCod;
            }
        }
    }

    return ActualRobots;
}


///funcion, bajo metodo.
robot getRobotfromSnapShot(RotatedRect _RecContorno)
{
    Mat SemiCropCodRotated, finalCropCodRotated;
    int tempID, tempX, tempY, tempTheta;
    float tempFloatX, tempFloatY, tempFloatTheta, tempWiMitad, tempHeMitad;
    cout << "inicie la toma de pose" << endl;
    tempWiMitad = SQRTDE2 *_RecContorno.size.width / 2;
    tempHeMitad = SQRTDE2 * _RecContorno.size.height / 2;
    //cout << "finalice los calculos" << endl;
    //Range rows((int)(_RecContorno.center.y - tempHeMitad), (int)(_RecContorno.center.y + tempHeMitad));
    //Range cols((int)(_RecContorno.center.x - tempWiMitad), (int)(_RecContorno.center.x + tempWiMitad));
    /*
    cout << "Obtuve el range" << endl;
    cout << rows << endl;
    cout << cols << endl;
    */
    Rect crop_region((int)(_RecContorno.center.y - tempHeMitad), (int)(_RecContorno.center.y + tempHeMitad),(int)(_RecContorno.center.x - tempWiMitad), (int)(_RecContorno.center.x + tempWiMitad));

    Mat SemiCropCod = GlobalCroppedActualSnap;
    //cout << "Corte la imagen" << endl;
    Mat tempRotMat = getRotationMatrix2D(_RecContorno.center, _RecContorno.angle, 1.0);
    warpAffine(SemiCropCod, SemiCropCodRotated, tempRotMat, SemiCropCod.size(), INTER_LINEAR);
    //cout << "Use la nueva matriz y encontre la nueva foto" << endl;
    getRectSubPix(SemiCropCodRotated, _RecContorno.size, _RecContorno.center, finalCropCodRotated);
    cvtColor(finalCropCodRotated, finalCropCodRotated, CV_BGR2GRAY, 0);
    //cout << "Le aplique filtro de blanco y negro" << endl;

    /*
    cout << "medidas de las fotos" << endl;
    cout << finalCropCodRotated.size() << endl;
    cout << finalCropCodRotated.size().width << endl;
    cout << finalCropCodRotated.size().height << endl;
    */

    //if ((finalCropCodRotated.size().width > 70) && (finalCropCodRotated.size().height > 70)) {

    //cout<< "A encontrar el codigo" << endl;
    int EscalaColores[3]; //[2] blaco, [1] gris, [0] negro
    int ColorSupIzq = finalCropCodRotated.at<uchar>(finalCropCodRotated.size().height * 1 / 4, finalCropCodRotated.size().width * 1 / 4);
    int ColorSupDer = finalCropCodRotated.at<uchar>(finalCropCodRotated.size().height * 1 / 4, finalCropCodRotated.size().width * 3 / 4);
    int ColorInfDer = finalCropCodRotated.at<uchar>(finalCropCodRotated.size().height * 3 / 4, finalCropCodRotated.size().width * 3 / 4);
    int ColorInfIzq = finalCropCodRotated.at<uchar>(finalCropCodRotated.size().height * 3 / 4, finalCropCodRotated.size().width * 1 / 4);
    EscalaColores[0] = EscalaColores[1] = EscalaColores[2] = ColorSupIzq;
    tempFloatTheta = _RecContorno.angle;

     //cout << "defini las esquinas" << endl;

     //cout<< "comparando las esquinas para encontrar el pivote" << endl;
    if ((ColorSupDer > ColorSupIzq) && (ColorSupDer > ColorInfDer) && (ColorSupDer > ColorInfIzq))
    {
        rotate(finalCropCodRotated, finalCropCodRotated, ROTATE_90_COUNTERCLOCKWISE);
        tempFloatTheta = tempFloatTheta + 90;
        EscalaColores[2] = ColorSupDer;
    }
    else if ((ColorInfDer > ColorSupIzq) && (ColorInfDer > ColorSupDer) && (ColorInfDer > ColorInfIzq))
    {
        rotate(finalCropCodRotated, finalCropCodRotated, ROTATE_180);
        tempFloatTheta = tempFloatTheta + 180;
        EscalaColores[2] = ColorInfDer;
    }
    else if ((ColorInfIzq > ColorSupIzq) && (ColorInfIzq > ColorInfDer) && (ColorInfIzq > ColorSupDer))
    {
        rotate(finalCropCodRotated, finalCropCodRotated, ROTATE_90_CLOCKWISE);
        tempFloatTheta = tempFloatTheta - 90;
        EscalaColores[2] = ColorInfIzq;
    }


      //cout << "actualizando esquinas y colores" << endl;
    if ((ColorSupIzq <= ColorSupDer) && (ColorSupIzq <= ColorInfDer) && (ColorSupIzq <= ColorInfIzq))
        EscalaColores[0] = ColorSupIzq;
    else if ((ColorSupDer <= ColorSupIzq) && (ColorSupDer <= ColorInfDer) && (ColorSupDer <= ColorInfIzq))
        EscalaColores[0] = ColorSupDer;
    else if ((ColorInfDer <= ColorSupDer) && (ColorInfDer <= ColorSupIzq) && (ColorInfDer <= ColorInfIzq))
        EscalaColores[0] = ColorInfDer;
    else
        EscalaColores[0] = ColorInfIzq;

    //cout << "a mostrar el codigo" << endl;
    //imshow("Codigo", finalCropCodRotated);
    //waitKey(0);

    int MatrizValColores[3][3];

     //cout << "Encontrando los valores de la matriz" << endl;
    for (int u = 1; u <= 3; ++u) {
        for (int v = 1; v <= 3; ++v) {
            int ValColorTemp = finalCropCodRotated.at<uchar>((finalCropCodRotated.size().height * u / 4), (finalCropCodRotated.size().width * v / 4));
            MatrizValColores[(u - 1)][(v - 1)] = ValColorTemp;
            if ((ValColorTemp < EscalaColores[2] - GlobalColorDifThreshold) && (ValColorTemp > EscalaColores[0] + GlobalColorDifThreshold)) {
                EscalaColores[1] = ValColorTemp;
            }
        }
    }

    //Extraemos el codigo binario
     //cout << "Extraemos el codigo binario" << endl;
    string CodigoBinString = "";
    for (int u = 0; u < 3; ++u) {
        for (int v = 0; v < 3; ++v) {
            if ((u == 0) && (v == 0))
                CodigoBinString = CodigoBinString;
            else if ((MatrizValColores[u][v] > EscalaColores[1] - GlobalColorDifThreshold) && (MatrizValColores[u][v] < EscalaColores[1] + GlobalColorDifThreshold))
                CodigoBinString = CodigoBinString + "1";
            else
                CodigoBinString = CodigoBinString + "0";
        }
    }

    //Guardamos los valores
    //cout << "guardamos los valores" << endl;
    tempID = binTxttoint(CodigoBinString);
    //cout << "este es el codigo encontrado" << endl;
    //cout << tempID << endl;
    tempFloatX = (anchoMesa / GlobalWidth) * _RecContorno.center.x;
    tempFloatY = (largoMesa / GlobalHeigth) * _RecContorno.center.y;
    //cout<<"Las posiciones son estas" << endl;
    //cout<<"PosX" << tempFloatX << endl;
    //cout<<"PosY" << tempFloatY << endl;
    tempX = (int)tempFloatX;
    tempY = (int)tempFloatY;
    //tempFloatTheta = tempFloatTheta * MyPI / 180;
    tempTheta = (int)tempFloatTheta;
    cout << "Termine la obtencion de pose" << endl;
    return robot(tempID,"", tempX, tempY, tempTheta);
   //}
    //return robot(0,"", 0, 0, 0);
}

/// TERMINA getRobotfromSnapShot

int getLambdaWiHe()
{

        int dummy;
        int n = 0;
        int pipe_Calib;		// for file descriptors
        double a;
        Mat temp_mat = Mat::zeros(3,3,CV_64F);
        //cout << temp_mat << endl;
        dummy = system("mkfifo /tmp/CalibtoPose"); 	// could be done separetely in each task,
        //dummy = system("mkfifo AtoB");	// or in a terminal

        //printf("Abriendo /tmp/CalibtoPose\n");
        if((pipe_Calib = open("/tmp/CalibtoPose", O_RDONLY)) < 0)
        {
                printf("pipe /tmp/CalibtoPose error\n");
                exit(-1);
        }
        cout << "Pipe abierto" << endl;

        while(n < 3)
        {

            if (n == 0){
                cout << "Leyendo la matriz" << endl;
            for (int i = 0; i <3; i++){
                for (int j=0; j < 3; j++){
                //sleep(1);
                /*
                cout << "matriz" << endl;
                cout << i << endl;
                cout << j << endl;
                */
                if(read(pipe_Calib, &a, sizeof(a)) < 0)
                {
                        printf("/tmp/CalibtoPose pipe read error\n");
                        exit(-1);
                }

                 temp_mat.at<double>(i,j) = a;

                    }
            }
            //cout << temp_mat << endl;
        }

       else if (n == 1){
                cout << "Voy a leer el Width" << endl;
                //sleep(1);
               if(read(pipe_Calib, &GlobalWidth, sizeof(GlobalWidth)) != sizeof(GlobalWidth))
                   {
                       cout <<"/tmp/CalibtoPose write error" << endl;;
                       exit(-1);
                   }
               //cout << "Width leido" << endl;
               //cout << GlobalWidth << endl;
               }

            else if (n == 2){
                cout << "Voy a leer el Heigth" << endl;
                //sleep(1);

                  if(read(pipe_Calib, &GlobalHeigth, sizeof(GlobalHeigth)) != sizeof(GlobalHeigth))
                      {
                          cout <<"/tmp/CalibtoPose write error" << endl;;
                          exit(-1);
                      }
                      //cout << GlobalHeigth << endl;
                  }

                //printf("Count TaskA: %d \n", counter);
                n++;
                //cout << temp_mat << endl;
}

        GlobalLambda = temp_mat;
        cout << "Listo" <<endl;
        //cout << temp_mat << endl;

    //GlobalLambda = readHomogenea();
    //Mat dims = readDims();
    //GlobalWidth = (int)dims.at<double>(0, 0);
    //GlobalHeigth = (int)dims.at<double>(1, 0);
        return 0;
}

Mat getCroppedSnapshot(Mat _snap)
{
    if (GlobalWidth == 0)
        getLambdaWiHe();
    Mat CropSnap;
    cout << "Ajustando la foto" <<endl;
    warpPerspective(_snap, CropSnap, GlobalLambda , { GlobalWidth, GlobalHeigth });
    cout << "Foto ajustada" <<endl;
    return CropSnap;
}
