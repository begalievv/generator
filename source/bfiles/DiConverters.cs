using App.Access;
using App.General;
using Microsoft.Extensions.DependencyInjection;
using PL.Base;
using PL.General;

namespace PL
{
    public class DiConverters
    {
        public static void AddConverters(IServiceCollection services)
        {

            @|template_diconverter|@
            
        }
    }
}
