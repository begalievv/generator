using PL.Base;
using System;
using System.Globalization;

namespace PL.General
{
    public class @|table_name|@Model : BaseModel
    {
        @|template_model|@

        public override bool IsNew()
        {
            return id == 0;
        }

    }
}
