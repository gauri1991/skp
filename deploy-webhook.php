<?php
/**
 * Webhook endpoint for GitHub deployment
 * Place this file in your cPanel public_html directory
 */

// Security token - change this to a secure random string
$secret_token = 'your-secret-deploy-token-here';

// Check authorization
$headers = getallheaders();
$auth_header = isset($headers['Authorization']) ? $headers['Authorization'] : '';

if ($auth_header !== 'Bearer ' . $secret_token) {
    http_response_code(401);
    die('Unauthorized');
}

// Path to your deployment script
$deploy_script = '/home/cpanelusername/sumithrakp.com/deploy.sh';

// Execute deployment
$output = shell_exec("cd /home/cpanelusername/sumithrakp.com && bash deploy.sh 2>&1");

// Log the deployment
$log_file = '/home/cpanelusername/deployment.log';
$log_entry = date('Y-m-d H:i:s') . " - Deployment triggered\n" . $output . "\n---\n";
file_put_contents($log_file, $log_entry, FILE_APPEND);

// Return response
header('Content-Type: application/json');
echo json_encode([
    'status' => 'success',
    'message' => 'Deployment completed',
    'timestamp' => date('Y-m-d H:i:s'),
    'output' => $output
]);
?>