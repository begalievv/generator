using Domain.Entities;
using Newtonsoft.Json;
using Newtonsoft.Json.Serialization;

namespace WebApi.Dtos
{
    public class Get@|table_name_pascal|@Response
    {
        @|dto_fields|@

        internal static Get@|table_name_pascal|@Response FromDomain(@|table_name_pascal|@ domain)
        {
            return new Get@|table_name_pascal|@Response
            {
                @|dto_map_get|@
            };
        }
    }

    public class Create@|table_name_pascal|@Request
    {
        @|dto_fields|@

        internal @|table_name_pascal|@ ToDomain()
        {
            return new @|table_name_pascal|@
            {
                @|dto_map_create_update|@
            };
        }
    }

    public class Update@|table_name_pascal|@Request
    {
        @|dto_fields|@

        internal @|table_name_pascal|@ ToDomain()
        {
            return new @|table_name_pascal|@
            {
                @|dto_map_create_update|@
            };
        }
    }
}
