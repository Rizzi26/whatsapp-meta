// Importar Express.js 
 const  express  =  require  (  'express'  ); 

 // Criar um aplicativo Express 
 const  app  =  express  (); 

 // Middleware para analisar corpos JSON 
app  .  use  (  express  .  json  ()); 

 // Definir porta e verify_token 
 const  port  =  process  .  env  .  PORT  ||   3000  ; 
 const  verifyToken  =  process  .  env  .  VERIFY_TOKEN  ; 

 // Rotear para solicitações GET 
app  .  get  (  '/'  ,   (  req  ,  res  )   =>   { 
   const   {   'hub.mode'  :  modo  ,   'hub.challenge'  :  desafio  ,   'hub.verify_token'  :  token  }   =  req  .  query  ; 

   if   (  modo  ===   'inscrever-se'   &&  token  ===  verifyToken  )   { 
    console  .  log  (  'WEBHOOK VERIFICADO'  ); 
    res  .  status  (  200  ).  enviar  (  desafio  ); 
   }   senão   { 
    res  .  status  (  403  ).  end  (); 
   } 
 }); 

 // Rota para solicitações POST 
app  .  post  (  '/'  ,   (  req  ,  res  )   =>   { 
   const  timestamp  =   nova   data  ().  toISOString  ().  replace  (  'T'  ,   ' '  ).  slice  (  0  ,   19  ); 
  console  .  log  (`  \n\n  Webhook  recebido $  {  timestamp  }  \n  `); 
  console  .  log  (  JSON  .  stringify  (  req  .  corpo  ,   nulo  ,   2  )); 
  res  .  status  (  200  ).  end  (); 
 }); 

 // Inicie o servidor 
aplicativo  .  ouvir  (  porta  ,   ()   =>   { 
  console  .  log  (`  \n  Escutando  na porta $  {  port  }  \n  `); 
 }); 
