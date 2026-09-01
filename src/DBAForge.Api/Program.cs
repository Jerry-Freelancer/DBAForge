using DBAForge.Application;
using DBAForge.Contracts;
using DBAForge.Infrastructure;
using Serilog;

var builder = WebApplication.CreateBuilder(args);

builder.Host.UseSerilog((_, _, loggerConfiguration) => loggerConfiguration
    .WriteTo.Console());

builder.Services
    .AddDBAForgeApplication()
    .AddDBAForgeInfrastructure();

builder.Services.AddHealthChecks();

var app = builder.Build();

app.UseSerilogRequestLogging();

app.MapGet("/health", () => Results.Ok(new HealthResponse("Healthy")))
    .WithName("GetHealth")
    .WithTags("System");

app.Run();

public partial class Program
{
}
