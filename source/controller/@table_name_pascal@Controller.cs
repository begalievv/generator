using Application.UseCases;
using Asp.Versioning;
using Domain.Entities;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using WebApi.Dtos;

namespace WebApi.Controllers.V1
{
    [ApiVersion("1.0")]
    [ApiController]
    [AllowAnonymous]
    [Route("api/v{version:apiVersion}/[controller]")]
    public class @|table_name_pascal|@Controller : BaseController<I@|table_name_pascal|@UseCase, @|table_name_pascal|@, Get@|table_name_pascal|@Response, Create@|table_name_pascal|@Request,
        Update@|table_name_pascal|@Request>
    {
        private readonly I@|table_name_pascal|@UseCase _@|table_name_pascal|@UseCase;

        public @|table_name_pascal|@Controller(I@|table_name_pascal|@UseCase @|table_name_pascal|@UseCase,
            ILogger<BaseController<I@|table_name_pascal|@UseCase, @|table_name_pascal|@, Get@|table_name_pascal|@Response, Create@|table_name_pascal|@Request,
                Update@|table_name_pascal|@Request>> logger)
            : base(@|table_name_pascal|@UseCase, logger)
        {
            _@|table_name_pascal|@UseCase = @|table_name_pascal|@UseCase;
        }

        protected override Get@|table_name_pascal|@Response EntityToDtoMapper(@|table_name_pascal|@ entity)
        {
            return Get@|table_name_pascal|@Response.FromDomain(entity);
        }

        protected override @|table_name_pascal|@ CreateRequestToEntity(Create@|table_name_pascal|@Request requestDto)
        {
            return requestDto.ToDomain();
        }

        protected override @|table_name_pascal|@ UpdateRequestToEntity(Update@|table_name_pascal|@Request requestDto)
        {
            return requestDto.ToDomain();
        }
        
        @|template_controller|@

    }
}