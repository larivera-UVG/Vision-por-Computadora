
#ifndef CALIBRACAM_H
#define CALIBRACAM_H

int * getWiHe(Point* esquina);
Mat getHomogenea(Point* esquina);
int* readWiHe();
float mayor2float(float x1, float x2);
float distancia2puntos(Point p1, Point p2);
Point* get_esquinas(Mat src, int valueCanny, void*);
void saveMat(string name,Mat src);





#endif // CALIBRACAM_H
