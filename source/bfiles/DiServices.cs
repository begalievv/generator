using Microsoft.Extensions.DependencyInjection;
using FileStorage.Files;
using Core.Abstraction;
using App.General;
using Communication;
using MassTransit;
using App.Access;

namespace App
{
    public static class DiServices
    {
        public static void AddServices(IServiceCollection services)
        {

            @|template_diservice|@

        }
    }
}