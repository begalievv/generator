using Application.Models;
using Application.Repositories;
using Domain.Entities;
using FluentResults;

namespace Application.UseCases
{
    public class @|table_name_pascal|@UseCases : BaseUseCases<@|table_name_pascal|@>, I@|table_name_pascal|@UseCase
    {
        private readonly IUnitOfWork _unitOfWork;
        protected override IBaseRepository<@|table_name_pascal|@> Repository => _unitOfWork.@|table_name_pascal|@Repository;

        public @|table_name_pascal|@UseCases(IUnitOfWork unitOfWork) : base(unitOfWork)
        {
            _unitOfWork = unitOfWork;
        }

        @|template_usecase|@
    }
}
