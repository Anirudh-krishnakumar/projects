#include<stdio.h>
#include<stdlib.h>
#include<string.h>
int main()
{
    FILE* kk;
    int con,total,total0,total1;
    char q;
    int ani,an,op;
    FILE* fp;
    FILE* df;
    int ran;
    FILE* pf;
    FILE* jk;
    int a,i,j;
    int n,tp;
    int price,gst;
    int a1,rice,m;int str;
    int n1;
    int price1,gst1;
    FILE* aa;
    FILE* bb;
    FILE* cc;
    printf("Already customer or not(y/n):");
    scanf("%c",&q);

    if(q=='y')
    {
        printf("Enter type(1/2/3):");
        scanf("%d",&str);
        if(str==1)
        {
            printf("No.of members in family:");
            scanf("%d",&j);
            printf("enter smart card no:");
            scanf("%d",&ani);
            kk=fopen("smart card no.txt","r");
for(i=0;i<"EOF";i++){
                fscanf(kk,"%d",&an);
                printf("%d",an);
                if(ani==an)
                {
                    fp=fopen("stock _sugar.txt","r+");
                    fscanf(fp,"%d",&n);
                    printf("stocks:%d\n",n);
                    pf=fopen("stock _sugar.txt","w");
                    int st;
                    st=j*5;
                    n-=st;
                    price=(st*10);
                    total0=price;
                    fprintf(pf,"%d\n",n);
                    printf("Remaing stocks:%d\n",n);

                    if(n<=0)
                    {
                        printf("out of stock\n");
                        printf("stock updation");
                        scanf("%d",&j);
                        j+=n;
                        jk=fopen("stock _sugar.txt","w");
                        fprintf(jk,"%d",j);
                        fscanf(jk,"%d",&j);
                    }

                    printf("any other products:");
                    scanf("%d",&con);
                    if(con==1)
                    {
                        aa=fopen("stock _rice.txt","r+");
                        fscanf(aa,"%d",&n1);
                        printf("stocks:%d\n",n1);
                        int fo;
                        fo=j*10;


                        n1-=fo;
                        total1=0;
                        printf("Remaing stocks:%d\n",n1);
                    }
                    if(n1<=0)
                    {
                        printf("stock updation:");
                        scanf("%d",&m);
                        j+=n1;
                        cc=fopen("stock _rice.txt","w");
                        fprintf(cc,"%d",m);
                        fscanf(cc,"%d",&m);
                    }
                    else
                    {
                        bb=fopen("stock _rice.txt","w");
                        fprintf(bb,"%d",n1);
                    }


                }
                else
                {



            } total=total0;
                printf("Total:%d",total);exit(1);
}





        if(str==2)
        {
            printf("No.of members in family:");
            scanf("%d",&j);
            printf("enter smart card no:");
            scanf("%d",&ani);
            kk=fopen("smart card no.txt","r");
            for(i=0; i<"EOF"; i++)
            {
                fscanf(kk,"%d",&an);
                if(ani==an)
                {




                    fp=fopen("stock _sugar.txt","r+");
                    fscanf(fp,"%d",&n);
                    printf("stocks:%d\n",n);
                    pf=fopen("stock _sugar.txt","w");
                    int st;
                    st=j*5;
                    n-=st;
                    price=(st*10);
                    total0=price;
                    fprintf(pf,"%d\n",n);
                    printf("Remaing stocks:%d\n",n);

                    if(n<=0)
                    {
                        printf("out of stock\n");
                        printf("stock updation");
                        scanf("%d",&j);
                        j+=n;
                        jk=fopen("stock _sugar.txt","w");
                        fprintf(jk,"%d",j);
                        fscanf(jk,"%d",&j);
                    }


                    total=total0;
                    printf("Total:%d",total);
                    exit(1);
                }
                else
                {
                    printf("Not match");
                    exit(1);
                }

            }

        }

        if(str==3)
        {
            printf("No.of members in family:");
            scanf("%d",&j);
            printf("enter smart card no:");
            scanf("%d",&ani);
            kk=fopen("smart card no.txt","r");
            for(i=0; i<"EOF"; i++)
            {
                fscanf(kk,"%d",&an);
                if(ani==an)
                {
                    printf("Just for identity");
                    exit(1);
                }
                else
                    exit(1);
            }
        }





    }
    else
    {
        printf("Creating a account");
        df=fopen("smart card no.txt","a");
        srand(time(0));
        ran=rand();
        fprintf(df,"%d\n",ran);
        printf("your smart card no;%d",ran);
    }


}

}
