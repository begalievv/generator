using Core.Abstraction;
using App.Base;
using System;
using System.Collections.Generic;
using System.Globalization;

namespace App.General
{
    public class CourseDto : IDtoWithId<int>
    {
        public int id { get; set; }
public string name { get; set; }
public DateTime? dateStart { get; set; }
public string strdateStart
{
get
{
return dateStart.HasValue ? dateStart.Value.ToString("yyyy-MM-dd") : null;
}
set
{
 dateStart = DateTime.ParseExact(value, "yyyy-MM-dd", CultureInfo.InvariantCulture);
}
}
public DateTime? dateEnd { get; set; }
public string strdateEnd
{
get
{
return dateEnd.HasValue ? dateEnd.Value.ToString("yyyy-MM-dd") : null;
}
set
{
 dateEnd = DateTime.ParseExact(value, "yyyy-MM-dd", CultureInfo.InvariantCulture);
}
}
public int idCourse { get; set; }
public int idGroup { get; set; }
public int idStatus { get; set; }

    }
}