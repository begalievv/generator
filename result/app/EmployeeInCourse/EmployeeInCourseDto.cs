using Core.Abstraction;
using App.Base;
using System;
using System.Collections.Generic;
using System.Globalization;

namespace App.General
{
    public class EmployeeInCourseDto : IDtoWithId<int>
    {
        public int id { get; set; }
public int idEmployee { get; set; }
public int idCourse { get; set; }
public int idPost { get; set; }

    }
}