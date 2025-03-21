using System.Data;
using Dapper;
using Domain.Entities;
using Application.Repositories;
using Infrastructure.Data.Models;
using Application.Exceptions;
using Application.Models;
using System;
using FluentResults;

namespace Infrastructure.Repositories
{
    public class @|table_name_pascal|@Repository : I@|table_name_pascal|@Repository
    {
        private readonly IDbConnection _dbConnection;
        private IDbTransaction? _dbTransaction;

        public @|table_name_pascal|@Repository(IDbConnection dbConnection)
        {
            _dbConnection = dbConnection;
        }

        public void SetTransaction(IDbTransaction dbTransaction)
        {
            _dbTransaction = dbTransaction;
        }

        public async Task<Result<List<@|table_name_pascal|@>>> GetAll()
        {
            try
            {
                var sql = @"
                    SELECT 
                        @|repo_get_all_fields|@
                    FROM ""@|table_name|@"";
                ";

                var models = await _dbConnection.QueryAsync<@|table_name_pascal|@>(sql, transaction: _dbTransaction);
                
                var results = models.Select(model => From@|table_name_pascal|@Model(model)).ToList();

                return Result.Ok(results);
            }
            catch (Exception ex)
            {
                return Result.Fail(new ExceptionalError("Failed to get all @|table_name|@", ex)
                    .WithMetadata("ErrorCode", "FETCH_ALL_FAILED"));
            }
        }

        public async Task<Result<@|table_name_pascal|@>> GetOneByID(int id)
        {
            try
            {
                var sql = @"
                    SELECT 
                        @|repo_get_all_fields|@
                    FROM ""@|table_name|@"" WHERE id=@Id;";
                var model = await _dbConnection.QuerySingleOrDefaultAsync<@|table_name_pascal|@>(sql, new { Id = id },
                    transaction: _dbTransaction);

                if (model == null)
                {
                    return Result.Fail(new ExceptionalError($"@|table_name_pascal|@ with ID {id} not found.", null)
                        .WithMetadata("ErrorCode", "NOT_FOUND"));
                }

                var result = From@|table_name_pascal|@Model(model);

                return Result.Ok(result);
            }
            catch (Exception ex)
            {
                return Result.Fail(new ExceptionalError("Failed to get @|table_name_pascal|@", ex)
                    .WithMetadata("ErrorCode", "FETCH_ONE_FAILED"));
            }
        }

        public async Task<Result<int>> Add(@|table_name_pascal|@ domain)
        {
            try
            {
                var model = To@|table_name_pascal|@Model(domain);

                var sql = @"
                    INSERT INTO ""@|table_name|@""(@|template_repo_create_fields|@) 
                    VALUES (@|template_repo_create_fields_values|@) RETURNING id
                ";

                var result = await _dbConnection.ExecuteScalarAsync<int>(sql, model, transaction: _dbTransaction);
                return Result.Ok(result);
            }
            catch (Exception ex)
            {
                return Result.Fail(new ExceptionalError("Failed to add @|table_name_pascal|@", ex)
                    .WithMetadata("ErrorCode", "ADD_FAILED"));
            }
        }

        public async Task<Result> Update(@|table_name_pascal|@ domain)
        {
            try
            {
                var model = To@|table_name_pascal|@Model(domain);

                var sql = @"
                    UPDATE ""@|table_name|@"" SET 
                    @|template_repo_update_fields|@ 
                    WHERE id = @Id";
                var affected = await _dbConnection.ExecuteAsync(sql, model, transaction: _dbTransaction);
                if (affected == 0)
                {
                    return Result.Fail(new ExceptionalError("Not found", null)
                        .WithMetadata("ErrorCode", "NOT_FOUND"));
                }

                return Result.Ok();
            }
            catch (Exception ex)
            {
                return Result.Fail(new ExceptionalError("Failed to update @|table_name_pascal|@", ex)
                    .WithMetadata("ErrorCode", "UPDATE_FAILED"));
            }
        }

        public async Task<Result<PaginatedList<@|table_name_pascal|@>>> GetPaginated(int pageSize, int pageNumber)
        {
            try
            {
                var sql = @"
                    SELECT 
                        @|repo_get_all_fields|@
                    FROM ""@|table_name|@""
                    OFFSET @pageSize * (@pageNumber - 1) Limit @pageSize;";
                var models = await _dbConnection.QueryAsync<@|table_name_pascal|@>(sql, new { pageSize, pageNumber },
                    transaction: _dbTransaction);

                var sqlCount = @"SELECT Count(*) FROM ""@|table_name|@""";
                var totalItems = await _dbConnection.ExecuteScalarAsync<int>(sqlCount, transaction: _dbTransaction);

                var results = models.Select(model => From@|table_name_pascal|@Model(model)).ToList();

                var domainItems = results;

                return Result.Ok(new PaginatedList<@|table_name_pascal|@>(domainItems, totalItems, pageNumber, pageSize));
            }
            catch (Exception ex)
            {
                return Result.Fail(new ExceptionalError("Failed to get @|table_name_pascal|@", ex)
                    .WithMetadata("ErrorCode", "FETCH_PAGINATED_FAILED"));
            }
        }

        public async Task<Result> Delete(int id)
        {
            try
            {
                var sql = @"DELETE FROM ""@|table_name|@"" WHERE id = @Id";
                var affected = await _dbConnection.ExecuteAsync(sql, new { Id = id }, transaction: _dbTransaction);

                if (affected == 0)
                {
                    return Result.Fail(new ExceptionalError("@|table_name_pascal|@ not found", null)
                        .WithMetadata("ErrorCode", "NOT_FOUND"));
                }

                return Result.Ok();
            }
            catch (Exception ex)
            {
                return Result.Fail(new ExceptionalError("Failed to delete @|table_name_pascal|@", ex)
                    .WithMetadata("ErrorCode", "DELETE_FAILED"));
            }
        }

        @|template_repository|@

        private @|table_name_pascal|@Model To@|table_name_pascal|@Model(@|table_name_pascal|@ model)
        {
            return new @|table_name_pascal|@Model
            {
                @|repo_model_converter|@
            };
        }

        private @|table_name_pascal|@ From@|table_name_pascal|@Model(@|table_name_pascal|@ model)
        {
            return new @|table_name_pascal|@
            {
                @|repo_model_converter|@
            };
        }
    }
}
