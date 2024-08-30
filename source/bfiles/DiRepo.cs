using Microsoft.Extensions.DependencyInjection;
using DAL.EF.Context;
using FileStorage.Files;
using Core.Abstraction;
using App;
using App.Base;
using App.General;
using DAL.General;
using App.Logic;
using App.Access;

namespace DAL
{
    public static class DiRepo
    {
        public static void AddRepos(IServiceCollection services)
        {

            @|template_direpo|@

        }
    }
}
