using DBAForge.Application;
using DBAForge.Contracts;
using DBAForge.Infrastructure;

var builder = WebApplication.CreateBuilder(args);

builder.Logging.ClearProviders();
builder.Logging.AddJsonConsole();

builder.Services
    .AddDBAForgeApplication()
    .AddDBAForgeInfrastructure();

builder.Services.AddHealthChecks();

var app = builder.Build();

app.MapGet("/health", () => Results.Ok(new HealthResponse("Healthy")))
    .WithName("GetHealth")
    .WithTags("System");

app.Run();

public partial class Program
{
}
