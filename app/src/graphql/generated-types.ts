import { GraphQLResolveInfo } from 'graphql';
export type Maybe<T> = T | null;
export type InputMaybe<T> = Maybe<T>;
export type Exact<T extends { [key: string]: unknown }> = { [K in keyof T]: T[K] };
export type MakeOptional<T, K extends keyof T> = Omit<T, K> & { [SubKey in K]?: Maybe<T[SubKey]> };
export type MakeMaybe<T, K extends keyof T> = Omit<T, K> & { [SubKey in K]: Maybe<T[SubKey]> };
export type MakeEmpty<T extends { [key: string]: unknown }, K extends keyof T> = { [_ in K]?: never };
export type Incremental<T> = T | { [P in keyof T]?: P extends ' $fragmentName' | '__typename' ? T[P] : never };
export type RequireFields<T, K extends keyof T> = Omit<T, K> & { [P in K]-?: NonNullable<T[P]> };
/** All built-in and custom scalars, mapped to their actual values */
export type Scalars = {
  ID: { input: string; output: string; }
  String: { input: string; output: string; }
  Boolean: { input: boolean; output: boolean; }
  Int: { input: number; output: number; }
  Float: { input: number; output: number; }
};

export type Book = {
  __typename?: 'Book';
  content: BookContent;
  id: Scalars['ID']['output'];
};

export type BookContent = {
  __typename?: 'BookContent';
  ISBN?: Maybe<Scalars['Int']['output']>;
  name: Scalars['String']['output'];
};

export type BookContentInput = {
  ISBN?: InputMaybe<Scalars['Int']['input']>;
  name: Scalars['String']['input'];
};

export type BookContentPatchInput = {
  ISBN?: InputMaybe<Scalars['Int']['input']>;
  name?: InputMaybe<Scalars['String']['input']>;
};

export type BookPatchInput = {
  content: BookContentPatchInput;
  id: Scalars['ID']['input'];
};

export type BookReplaceInput = {
  content: BookContentInput;
  id: Scalars['ID']['input'];
};

export type BooksDeleteResponse = {
  __typename?: 'BooksDeleteResponse';
  deletedIds: Array<Maybe<Scalars['ID']['output']>>;
  errors: Array<Maybe<ErrorResponse>>;
};

export type BooksListFiltersInput = {
  name?: InputMaybe<Scalars['String']['input']>;
};

export type BooksListInput = {
  filters?: InputMaybe<BooksListFiltersInput>;
};

export type BooksListResponse = {
  __typename?: 'BooksListResponse';
  code?: Maybe<Scalars['Int']['output']>;
  message: Scalars['String']['output'];
  records?: Maybe<Array<Maybe<Book>>>;
};

export type BooksResponse = {
  __typename?: 'BooksResponse';
  errors: Array<Maybe<ErrorResponse>>;
  records: Array<Maybe<Book>>;
};

export type ErrorResponse = {
  __typename?: 'ErrorResponse';
  code: Scalars['Int']['output'];
  id?: Maybe<Scalars['ID']['output']>;
  message: Scalars['String']['output'];
};

export type LoginResponse = {
  __typename?: 'LoginResponse';
  status?: Maybe<Status>;
  token?: Maybe<Scalars['String']['output']>;
  user?: Maybe<User>;
};

export type Mutation = {
  __typename?: 'Mutation';
  authLoginGoogle: LoginResponse;
  authSignUpGoogle: LoginResponse;
  booksCreate?: Maybe<BooksResponse>;
  booksDelete?: Maybe<BooksDeleteResponse>;
  booksPatch?: Maybe<BooksResponse>;
  booksReplace?: Maybe<BooksResponse>;
};


export type MutationAuthLoginGoogleArgs = {
  credential: Scalars['String']['input'];
};


export type MutationAuthSignUpGoogleArgs = {
  credential: Scalars['String']['input'];
};


export type MutationBooksCreateArgs = {
  contents: Array<InputMaybe<BookContentInput>>;
};


export type MutationBooksDeleteArgs = {
  ids: Array<InputMaybe<Scalars['ID']['input']>>;
};


export type MutationBooksPatchArgs = {
  records: Array<InputMaybe<BookPatchInput>>;
};


export type MutationBooksReplaceArgs = {
  records: Array<InputMaybe<BookReplaceInput>>;
};

export type Query = {
  __typename?: 'Query';
  booksGetByIds?: Maybe<BooksResponse>;
  booksList?: Maybe<BooksListResponse>;
};


export type QueryBooksGetByIdsArgs = {
  ids: Array<Scalars['ID']['input']>;
};


export type QueryBooksListArgs = {
  query?: InputMaybe<BooksListInput>;
};

export type Status = {
  __typename?: 'Status';
  code: Scalars['Int']['output'];
  codeName: Scalars['String']['output'];
  message: Scalars['String']['output'];
};

export type User = {
  __typename?: 'User';
  content?: Maybe<UserContent>;
  id: Scalars['ID']['output'];
};

export type UserContent = {
  __typename?: 'UserContent';
  email: Scalars['String']['output'];
  firstName: Scalars['String']['output'];
  lastName: Scalars['String']['output'];
};

export type WithIndex<TObject> = TObject & Record<string, any>;
export type ResolversObject<TObject> = WithIndex<TObject>;

export type ResolverTypeWrapper<T> = Promise<T> | T;


export type ResolverWithResolve<TResult, TParent, TContext, TArgs> = {
  resolve: ResolverFn<TResult, TParent, TContext, TArgs>;
};
export type Resolver<TResult, TParent = {}, TContext = {}, TArgs = {}> = ResolverFn<TResult, TParent, TContext, TArgs> | ResolverWithResolve<TResult, TParent, TContext, TArgs>;

export type ResolverFn<TResult, TParent, TContext, TArgs> = (
  parent: TParent,
  args: TArgs,
  context: TContext,
  info: GraphQLResolveInfo
) => Promise<TResult> | TResult;

export type SubscriptionSubscribeFn<TResult, TParent, TContext, TArgs> = (
  parent: TParent,
  args: TArgs,
  context: TContext,
  info: GraphQLResolveInfo
) => AsyncIterable<TResult> | Promise<AsyncIterable<TResult>>;

export type SubscriptionResolveFn<TResult, TParent, TContext, TArgs> = (
  parent: TParent,
  args: TArgs,
  context: TContext,
  info: GraphQLResolveInfo
) => TResult | Promise<TResult>;

export interface SubscriptionSubscriberObject<TResult, TKey extends string, TParent, TContext, TArgs> {
  subscribe: SubscriptionSubscribeFn<{ [key in TKey]: TResult }, TParent, TContext, TArgs>;
  resolve?: SubscriptionResolveFn<TResult, { [key in TKey]: TResult }, TContext, TArgs>;
}

export interface SubscriptionResolverObject<TResult, TParent, TContext, TArgs> {
  subscribe: SubscriptionSubscribeFn<any, TParent, TContext, TArgs>;
  resolve: SubscriptionResolveFn<TResult, any, TContext, TArgs>;
}

export type SubscriptionObject<TResult, TKey extends string, TParent, TContext, TArgs> =
  | SubscriptionSubscriberObject<TResult, TKey, TParent, TContext, TArgs>
  | SubscriptionResolverObject<TResult, TParent, TContext, TArgs>;

export type SubscriptionResolver<TResult, TKey extends string, TParent = {}, TContext = {}, TArgs = {}> =
  | ((...args: any[]) => SubscriptionObject<TResult, TKey, TParent, TContext, TArgs>)
  | SubscriptionObject<TResult, TKey, TParent, TContext, TArgs>;

export type TypeResolveFn<TTypes, TParent = {}, TContext = {}> = (
  parent: TParent,
  context: TContext,
  info: GraphQLResolveInfo
) => Maybe<TTypes> | Promise<Maybe<TTypes>>;

export type IsTypeOfResolverFn<T = {}, TContext = {}> = (obj: T, context: TContext, info: GraphQLResolveInfo) => boolean | Promise<boolean>;

export type NextResolverFn<T> = () => Promise<T>;

export type DirectiveResolverFn<TResult = {}, TParent = {}, TContext = {}, TArgs = {}> = (
  next: NextResolverFn<TResult>,
  parent: TParent,
  args: TArgs,
  context: TContext,
  info: GraphQLResolveInfo
) => TResult | Promise<TResult>;



/** Mapping between all available schema types and the resolvers types */
export type ResolversTypes = ResolversObject<{
  Book: ResolverTypeWrapper<Book>;
  BookContent: ResolverTypeWrapper<BookContent>;
  BookContentInput: BookContentInput;
  BookContentPatchInput: BookContentPatchInput;
  BookPatchInput: BookPatchInput;
  BookReplaceInput: BookReplaceInput;
  BooksDeleteResponse: ResolverTypeWrapper<BooksDeleteResponse>;
  BooksListFiltersInput: BooksListFiltersInput;
  BooksListInput: BooksListInput;
  BooksListResponse: ResolverTypeWrapper<BooksListResponse>;
  BooksResponse: ResolverTypeWrapper<BooksResponse>;
  Boolean: ResolverTypeWrapper<Scalars['Boolean']['output']>;
  ErrorResponse: ResolverTypeWrapper<ErrorResponse>;
  ID: ResolverTypeWrapper<Scalars['ID']['output']>;
  Int: ResolverTypeWrapper<Scalars['Int']['output']>;
  LoginResponse: ResolverTypeWrapper<LoginResponse>;
  Mutation: ResolverTypeWrapper<{}>;
  Query: ResolverTypeWrapper<{}>;
  Status: ResolverTypeWrapper<Status>;
  String: ResolverTypeWrapper<Scalars['String']['output']>;
  User: ResolverTypeWrapper<User>;
  UserContent: ResolverTypeWrapper<UserContent>;
}>;

/** Mapping between all available schema types and the resolvers parents */
export type ResolversParentTypes = ResolversObject<{
  Book: Book;
  BookContent: BookContent;
  BookContentInput: BookContentInput;
  BookContentPatchInput: BookContentPatchInput;
  BookPatchInput: BookPatchInput;
  BookReplaceInput: BookReplaceInput;
  BooksDeleteResponse: BooksDeleteResponse;
  BooksListFiltersInput: BooksListFiltersInput;
  BooksListInput: BooksListInput;
  BooksListResponse: BooksListResponse;
  BooksResponse: BooksResponse;
  Boolean: Scalars['Boolean']['output'];
  ErrorResponse: ErrorResponse;
  ID: Scalars['ID']['output'];
  Int: Scalars['Int']['output'];
  LoginResponse: LoginResponse;
  Mutation: {};
  Query: {};
  Status: Status;
  String: Scalars['String']['output'];
  User: User;
  UserContent: UserContent;
}>;

export type BookResolvers<ContextType = any, ParentType extends ResolversParentTypes['Book'] = ResolversParentTypes['Book']> = ResolversObject<{
  content?: Resolver<ResolversTypes['BookContent'], ParentType, ContextType>;
  id?: Resolver<ResolversTypes['ID'], ParentType, ContextType>;
  __isTypeOf?: IsTypeOfResolverFn<ParentType, ContextType>;
}>;

export type BookContentResolvers<ContextType = any, ParentType extends ResolversParentTypes['BookContent'] = ResolversParentTypes['BookContent']> = ResolversObject<{
  ISBN?: Resolver<Maybe<ResolversTypes['Int']>, ParentType, ContextType>;
  name?: Resolver<ResolversTypes['String'], ParentType, ContextType>;
  __isTypeOf?: IsTypeOfResolverFn<ParentType, ContextType>;
}>;

export type BooksDeleteResponseResolvers<ContextType = any, ParentType extends ResolversParentTypes['BooksDeleteResponse'] = ResolversParentTypes['BooksDeleteResponse']> = ResolversObject<{
  deletedIds?: Resolver<Array<Maybe<ResolversTypes['ID']>>, ParentType, ContextType>;
  errors?: Resolver<Array<Maybe<ResolversTypes['ErrorResponse']>>, ParentType, ContextType>;
  __isTypeOf?: IsTypeOfResolverFn<ParentType, ContextType>;
}>;

export type BooksListResponseResolvers<ContextType = any, ParentType extends ResolversParentTypes['BooksListResponse'] = ResolversParentTypes['BooksListResponse']> = ResolversObject<{
  code?: Resolver<Maybe<ResolversTypes['Int']>, ParentType, ContextType>;
  message?: Resolver<ResolversTypes['String'], ParentType, ContextType>;
  records?: Resolver<Maybe<Array<Maybe<ResolversTypes['Book']>>>, ParentType, ContextType>;
  __isTypeOf?: IsTypeOfResolverFn<ParentType, ContextType>;
}>;

export type BooksResponseResolvers<ContextType = any, ParentType extends ResolversParentTypes['BooksResponse'] = ResolversParentTypes['BooksResponse']> = ResolversObject<{
  errors?: Resolver<Array<Maybe<ResolversTypes['ErrorResponse']>>, ParentType, ContextType>;
  records?: Resolver<Array<Maybe<ResolversTypes['Book']>>, ParentType, ContextType>;
  __isTypeOf?: IsTypeOfResolverFn<ParentType, ContextType>;
}>;

export type ErrorResponseResolvers<ContextType = any, ParentType extends ResolversParentTypes['ErrorResponse'] = ResolversParentTypes['ErrorResponse']> = ResolversObject<{
  code?: Resolver<ResolversTypes['Int'], ParentType, ContextType>;
  id?: Resolver<Maybe<ResolversTypes['ID']>, ParentType, ContextType>;
  message?: Resolver<ResolversTypes['String'], ParentType, ContextType>;
  __isTypeOf?: IsTypeOfResolverFn<ParentType, ContextType>;
}>;

export type LoginResponseResolvers<ContextType = any, ParentType extends ResolversParentTypes['LoginResponse'] = ResolversParentTypes['LoginResponse']> = ResolversObject<{
  status?: Resolver<Maybe<ResolversTypes['Status']>, ParentType, ContextType>;
  token?: Resolver<Maybe<ResolversTypes['String']>, ParentType, ContextType>;
  user?: Resolver<Maybe<ResolversTypes['User']>, ParentType, ContextType>;
  __isTypeOf?: IsTypeOfResolverFn<ParentType, ContextType>;
}>;

export type MutationResolvers<ContextType = any, ParentType extends ResolversParentTypes['Mutation'] = ResolversParentTypes['Mutation']> = ResolversObject<{
  authLoginGoogle?: Resolver<ResolversTypes['LoginResponse'], ParentType, ContextType, RequireFields<MutationAuthLoginGoogleArgs, 'credential'>>;
  authSignUpGoogle?: Resolver<ResolversTypes['LoginResponse'], ParentType, ContextType, RequireFields<MutationAuthSignUpGoogleArgs, 'credential'>>;
  booksCreate?: Resolver<Maybe<ResolversTypes['BooksResponse']>, ParentType, ContextType, RequireFields<MutationBooksCreateArgs, 'contents'>>;
  booksDelete?: Resolver<Maybe<ResolversTypes['BooksDeleteResponse']>, ParentType, ContextType, RequireFields<MutationBooksDeleteArgs, 'ids'>>;
  booksPatch?: Resolver<Maybe<ResolversTypes['BooksResponse']>, ParentType, ContextType, RequireFields<MutationBooksPatchArgs, 'records'>>;
  booksReplace?: Resolver<Maybe<ResolversTypes['BooksResponse']>, ParentType, ContextType, RequireFields<MutationBooksReplaceArgs, 'records'>>;
}>;

export type QueryResolvers<ContextType = any, ParentType extends ResolversParentTypes['Query'] = ResolversParentTypes['Query']> = ResolversObject<{
  booksGetByIds?: Resolver<Maybe<ResolversTypes['BooksResponse']>, ParentType, ContextType, RequireFields<QueryBooksGetByIdsArgs, 'ids'>>;
  booksList?: Resolver<Maybe<ResolversTypes['BooksListResponse']>, ParentType, ContextType, Partial<QueryBooksListArgs>>;
}>;

export type StatusResolvers<ContextType = any, ParentType extends ResolversParentTypes['Status'] = ResolversParentTypes['Status']> = ResolversObject<{
  code?: Resolver<ResolversTypes['Int'], ParentType, ContextType>;
  codeName?: Resolver<ResolversTypes['String'], ParentType, ContextType>;
  message?: Resolver<ResolversTypes['String'], ParentType, ContextType>;
  __isTypeOf?: IsTypeOfResolverFn<ParentType, ContextType>;
}>;

export type UserResolvers<ContextType = any, ParentType extends ResolversParentTypes['User'] = ResolversParentTypes['User']> = ResolversObject<{
  content?: Resolver<Maybe<ResolversTypes['UserContent']>, ParentType, ContextType>;
  id?: Resolver<ResolversTypes['ID'], ParentType, ContextType>;
  __isTypeOf?: IsTypeOfResolverFn<ParentType, ContextType>;
}>;

export type UserContentResolvers<ContextType = any, ParentType extends ResolversParentTypes['UserContent'] = ResolversParentTypes['UserContent']> = ResolversObject<{
  email?: Resolver<ResolversTypes['String'], ParentType, ContextType>;
  firstName?: Resolver<ResolversTypes['String'], ParentType, ContextType>;
  lastName?: Resolver<ResolversTypes['String'], ParentType, ContextType>;
  __isTypeOf?: IsTypeOfResolverFn<ParentType, ContextType>;
}>;

export type Resolvers<ContextType = any> = ResolversObject<{
  Book?: BookResolvers<ContextType>;
  BookContent?: BookContentResolvers<ContextType>;
  BooksDeleteResponse?: BooksDeleteResponseResolvers<ContextType>;
  BooksListResponse?: BooksListResponseResolvers<ContextType>;
  BooksResponse?: BooksResponseResolvers<ContextType>;
  ErrorResponse?: ErrorResponseResolvers<ContextType>;
  LoginResponse?: LoginResponseResolvers<ContextType>;
  Mutation?: MutationResolvers<ContextType>;
  Query?: QueryResolvers<ContextType>;
  Status?: StatusResolvers<ContextType>;
  User?: UserResolvers<ContextType>;
  UserContent?: UserContentResolvers<ContextType>;
}>;

