// Andre Rodas
// Obtiene las esquinas de la mesa mediante los marcadores verdes

#include "opencv2/highgui/highgui.hpp"
#include "opencv2/imgproc/imgproc.hpp"
#include <iostream>
#include <stdio.h>
#include <stdlib.h>

using namespace cv;
using namespace std;

Mat src; Mat src_gray;
int max_thresh = 255;
VideoCapture cam(0);
Point esquina[4];
Mat pic;

/// Function header
void get_esquinas(Mat src, int valueCanny, void*);

Mat takePicture() {
    cam.set(CV_CAP_PROP_FRAME_WIDTH, 1280); //640
    cam.set(CV_CAP_PROP_FRAME_HEIGHT, 720); //480
    cam.set(CAP_PROP_AUTOFOCUS, 0); // turn the autofocus off
    while (!cam.isOpened()) {
        std::cout << "Failed to make connection to cam" << std::endl;
        cam.open(0);
    }
    cam >> pic;
    return pic;
}

float distancia(Point p1, Point p2)
{
    int distancex = (p2.x - p1.x) * (p2.x - p1.x);
    int distancey = (p2.y - p1.y) * (p2.y - p1.y);

    float distance = (sqrt(distancex + distancey) + 0.5);

    return distance;
}

void MyLine(Mat img, Point start, Point end)
{
    int thickness = 2;
    int lineType = 8;
    line(img, start, end,
        Scalar(0, 255, 255),
        thickness,
        lineType);
}

float mayor2float(float x1, float x2)
{
    if (x1 > x2)
        return x1;
    else
        return x2;
}



/** @function main */
int main(int argc, char** argv)
{
    namedWindow("original", CV_WINDOW_AUTOSIZE);
    namedWindow("canny", CV_WINDOW_AUTOSIZE);
    //namedWindow("filtro", CV_WINDOW_AUTOSIZE);
    /// Load source image and convert it to gray
    while ((char)waitKey(1) != 'q') {
        src = takePicture();
        imshow("canny", src);
        /// Convert image to gray and blur it
        //createTrackbar(" Adaptativo thresh:", "adaptativo", &thresh, max_thresh, esquinas);
        //createTrackbar(" canny thresh:", "canny", &thresh2, max_thresh, esquinas);
        get_esquinas(src, 95, 0);

        Mat lambda = Mat::eye(3, 3, CV_64F);
        float W1 = distancia(esquina[0], esquina[2]);
        float W2 = distancia(esquina[1], esquina[3]);
        W1 = mayor2float(W1, W2);
        float H1 = distancia(esquina[0], esquina[1]);
        float H2 = distancia(esquina[2], esquina[3]);
        H1 = mayor2float(H1, H2);
        Point2f esquinaFloat[4] = { esquina[0],esquina[2],esquina[1] ,esquina[3] };
        Point2f esquinasFinales[4] = { { 0, 0 },{ W1, 0 },{ 0,H1 },{ W1, H1 } };
        lambda = cv::getPerspectiveTransform(esquinaFloat, esquinasFinales);
        warpPerspective(src, src, lambda, { (int)W1,(int)H1 });
        imshow("original", src);
        //waitKey(0);
    }
    return(0);
}



/** @function para obtener esquinas */
void get_esquinas(Mat src,int valueCanny, void*)
{
    Mat canny_out;
    vector<vector<Point> > contours;
    vector<Vec4i> hierarchy;

    cvtColor(src, src_gray, CV_BGR2GRAY, 0);
    blur(src_gray, src_gray, Size(3, 3));
    Canny(src_gray, canny_out, valueCanny, valueCanny * 2, 3);
    findContours(canny_out, contours, hierarchy, CV_RETR_TREE, CV_CHAIN_APPROX_SIMPLE, Point(0, 0));

    /// Draw contours
    Mat drawing = Mat::zeros(canny_out.size(), CV_8UC3);
    bool a = true;

    Point bordesMAX[4] = { Point(0, 0) , Point(0, drawing.size().height) , Point(drawing.size().width, 0) , Point(drawing.size().width, drawing.size().height) };

    for (int i = 0; i< contours.size(); i++)
    {
        RotatedRect cod;
        cod = minAreaRect(contours[i]);
        if ((abs(cod.size.width - cod.size.height)<2) && ((cod.size.height > 8 && cod.size.height < 15) && (cod.size.width > 8 && cod.size.width < 15))) {
            if (a) {
                for (int i = 0; i < 4; i++)
                    esquina[i] = cod.center;
                a = false;
            }
            else {
                for (int i = 0; i < 4; i++)
                    if (distancia(bordesMAX[i], cod.center)<distancia(bordesMAX[i], esquina[i]))
                        esquina[i] = cod.center;
            }
        }
    }


    circle(drawing, esquina[0], 8, Scalar(255, 255, 255), CV_FILLED, 8, 0); ///Se dibujan los centros
    circle(drawing, esquina[1], 8, Scalar(255, 255, 255), CV_FILLED, 8, 0); ///Se dibujan los centros
    circle(drawing, esquina[2], 8, Scalar(255, 255, 255), CV_FILLED, 8, 0); ///Se dibujan los centros
    circle(drawing, esquina[3], 8, Scalar(255, 255, 255), CV_FILLED, 8, 0); ///Se dibujan los centros

    MyLine(drawing, esquina[0], esquina[1]);
    MyLine(drawing, esquina[1], esquina[3]);
    MyLine(drawing, esquina[3], esquina[2]);
    MyLine(drawing, esquina[2], esquina[0]);


    /// Show in a window


    //imshow("adaptativo", adaptative_out);
}
