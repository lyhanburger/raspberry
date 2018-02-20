#include "teacher_main.h"
#include "ui_teacher_main.h"

teacher_main::teacher_main(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::teacher_main)
{
    ui->setupUi(this);
}

teacher_main::~teacher_main()
{
    delete ui;
}
