<?php



/********************************
 * Autodiscover responder
 ********************************
 * This PHP script is intended to respond to any request to http(s)://mydomain.com/autodiscover/autodiscover.xml.
 * If configured properly, it will send a spec-complient autodiscover XML response, pointing mail clients to the
 * appropriate mail services.
 * If you use MAPI or ActiveSync, stick with the Autodiscover service your mail server provides for you. But if
 * you use POP/IMAP servers, this will provide autoconfiguration to Outlook, Apple Mail and mobile devices.
 *
 * To work properly, you'll need to set the service (sub)domains below in the settings section to the correct
 * domain names, adjust ports and SSL.
 */


$request = file_get_contents("php://input");


# file_put_contents( 'request.log', $request, FILE_APPEND );


preg_match( "/\<EMailAddress\>(.*?)\<\/EMailAddress\>/", $request, $email );


if (filter_var($email[1], FILTER_VALIDATE_EMAIL) === false) {
	throw new Exception('Invalid E-Mail provided');
}


$domain = substr( strrchr( $email[1], "@" ), 1 );

/**************************************
 *   Port and server settings below   *
 **************************************/


$imapServer = 'imap.' . $domain; // imap.example.com
$imapPort   = 993;
$imapSSL    = true;


$smtpServer = 'smtp.' . $domain; // smtp.example.com
$smtpPort   = 587;
$smtpSSL    = true;


header( 'Content-Type: application/xml' );
?>
<?php echo '<?xml version="1.0" encoding="utf-8" ?>'; ?>
<Autodiscover xmlns="http://schemas.microsoft.com/exchange/autodiscover/responseschema/2006" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" >
	<Response xmlns="http://schemas.microsoft.com/exchange/autodiscover/outlook/responseschema/2006a">
		<Account>
			<AccountType>email</AccountType>
			<Action>settings</Action>
			<Protocol>
			<Protocol>
				<Type>IMAP</Type>
				<Server><?php echo $imapServer; ?></Server>
				<Port><?php echo $imapPort; ?></Port>
				<DomainRequired>off</DomainRequired>
				<LoginName><?php echo $email[1]; ?></LoginName>
				<SPA>off</SPA>
				<SSL><?php echo $imapSSL ? 'on' : 'off'; ?></SSL>
				<AuthRequired>on</AuthRequired>
			</Protocol>
			<Protocol>
				<Type>SMTP</Type>
				<Server><?php echo $smtpServer; ?></Server>
				<Port><?php echo $smtpPort; ?></Port>
				<DomainRequired>off</DomainRequired>
				<LoginName><?php echo $email[1]; ?></LoginName>
				<SPA>off</SPA>
				<SSL><?php echo $smtpSSL ? 'on' : 'off'; ?></SSL>
				<AuthRequired>on</AuthRequired>
				<UsePOPAuth>on</UsePOPAuth>
				<SMTPLast>on</SMTPLast>
			</Protocol>
		</Account>
	</Response>
</Autodiscover>
