using App.General;
using DAL.EF.Entities;
using System.Linq;

namespace DAL.General
{
    static partial class @|table_name|@DtoConverter
    {
        public static @|table_name|@Dto To@|table_name|@Dto(this @|table_name|@ _@|table_name|@)
        {
            var result = new @|table_name|@Dto
            {
                @|template_toDto|@
            };
            return result;
        }
        public static @|table_name|@ To@|table_name|@(this @|table_name|@Dto dto)
        {
            var result = new @|table_name|@
            {
                @|template_toEntity|@
            };
            return result;
        }
    }
}
