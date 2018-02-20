#ifndef TEACHER_MAIN_H
#define TEACHER_MAIN_H

#include <QMainWindow>

namespace Ui {
class teacher_main;
}

class teacher_main : public QMainWindow
{
    Q_OBJECT

public:
    explicit teacher_main(QWidget *parent = 0);
    ~teacher_main();

private:
    Ui::teacher_main *ui;
};

#endif // TEACHER_MAIN_H
