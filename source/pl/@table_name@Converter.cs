using App.General;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using PL.Base;

namespace PL.General
{
    public class @|table_name|@Converter : IModelConverter<@|table_name|@Model, @|table_name|@Dto>
    {
        public @|table_name|@Dto ToDto(@|table_name|@Model model)
        {
            var result = new @|table_name|@Dto
            {
                @|template_converter|@
            };
            return result;
        }
    }
}
